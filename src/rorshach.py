"""
rorshach.py:
Creates and manages processes for each phrase supplied by the user, calling dual_forces.darken() on each one.
Waits for these processes to complete before turning each grid saved in grids.pkl into a png image.
Monitors progress so the user doesn't suspect the application is frozen or doing nothing.
"""

import random, multiprocessing, pickle, time, threading
import tkinter as tk
from PIL import Image, ImageFilter
from multiprocessing.managers import SyncManager
from sys import exc_info
import dual_forces


def gen_grid(phrases, blur=0, width=480, height=360):
    # shuffle phrases, prepare for multiprocessing:
    random.shuffle(phrases)
    processors = multiprocessing.cpu_count()
    m = SyncManager()
    m.start()
    progress = m.dict()
    #
    # begin constructing progress monitor:
    monitor = tk.Toplevel()
    monitor.title('Progress Monitor')
    tk.Label(monitor, text='Codename:').grid(row=1, column=1)
    tk.Label(monitor, text='Phrase factored into image x times:').grid(row=1, column=2)
    #
    # create a Process instance and set of labels for each phrase:
    jobs = []
    labels = []
    rownum = 1
    for phrase in phrases:
        rownum += 1
        codename = hex(hash(phrase))[2:]
        name = tk.Label(monitor, text=codename)
        name.grid(row=rownum, column=1)
        numb = tk.Label(monitor, text=0)
        numb.grid(row=rownum, column=2)
        labels.append([name, numb])
        progress[codename] = 0
        p = multiprocessing.Process(target=dual_forces.darken, args=(phrase, progress, width//2, height))
        jobs.append(p)
    #
    # set the Processes and progress monitor into motion:
    running_jobs = []
    for x in range(processors-1):
        try:
            jobs[x].start()
            running_jobs.append(jobs[x])
            jobs.remove(jobs[x])
        except IndexError:
            break
    threading.Thread(target=updater, args=(running_jobs, labels, progress)).start()
    while jobs:
        time.sleep(1)
        for x in running_jobs:
            if not x.is_alive():
                running_jobs.remove(x)
                jobs[0].start()
                running_jobs.append(jobs[0])
                jobs.remove(jobs[0])
                break
    for x in running_jobs:
        x.join()
    #
    # retrieve the grids, turn them into images and yield them and their codename:
    with open('grids.pkl', 'rb') as f:
        grids = pickle.load(f)
        for x in grids:
            img = inkblot(x[0], x[1], blur, width, height)
            yield img, x[2]


def inkblot(grid, inverse, blur, width, height):
    # create an image, use grid to fill in its pixels:
    img1 = Image.new('L', (width//2, height), color=255)
    pic1 = img1.load()
    for y in range(img1.size[1]):
        for x in range(img1.size[0]):
            if grid[y][x] == 1:
                pic1[x,y] = 0
            else:
                pic1[x,y] = 255
    # fixes a weird bug that I couldn't seem to resolve any other way
    img1, pic1 = extend(img1, pic1, 'l')
    #
    # do the same, but for the inverse grid:
    img2 = Image.new('L', (width//2, height), color=255)
    pic2 = img2.load()
    for y in range(img2.size[1]):
        for x in range(img2.size[0]):
            if inverse[y][x] == 1:
                pic2[x,y] = 0
            else:
                pic2[x,y] = 255
    # fixes a weird bug that I couldn't seem to resolve any other way
    img2, pic2 = extend(img2, pic2, 'r')
    #
    # combine the images:
    fusion = Image.new('L', (width, height), color=255)
    fusion.paste(img1)
    fusion.paste(img2, box=(width//2, 0))
    #
    # make the less pixelated if the user requested it:
    if blur == 1:
        fusion = fusion.filter(ImageFilter.SMOOTH)
    elif blur == 2:
        fusion = fusion.filter(ImageFilter.SMOOTH_MORE)
    elif blur == 3:
        fusion = fusion.filter(ImageFilter.SMOOTH_MORE)
        fusion = fusion.filter(ImageFilter.SMOOTH_MORE)
    #
    return fusion


def extend(img, pic, lr):
    # fixes a bug where the image has blank lines on 2 of the edges
    # I tried every other way I could think of to fix it...didn't work out.
    width = img.size[0]
    height = img.size[1]
    if lr == 'l':
        for y in range(height):
            if pic[width-2, y] == 0:
                pic[width-1, y] = 0
        for x in range(width):
            if pic[x, height-2] == 0:
                pic[x, height-1] = 0
    elif lr == 'r':
        for y in range(height):
            if pic[1, y] == 0:
                pic[0, y] = 0
        for x in range(width):
            if pic[x, 1] == 0:
                pic[x, 0] = 0
    return img, pic


def updater(running_jobs, labels, progress):
    # update the number of impressions for each image until jobs are done
    while True:
        time.sleep(0.5)
        try:
            for x in progress.keys():
                for y in labels:
                    if y[0].cget('text') == x:
                        y[1].configure(text=progress[x])
        except Exception:
            pass
        if still_alive(running_jobs):
            continue
        else:
            break
    #
    # then do it one last time:
    for x in progress.keys():
        for y in labels:
            if y[0].cget('text') == x:
                y[1].configure(text=progress[x])


def still_alive(running_jobs):
    # check to see if jobs are all done:
    for x in running_jobs:
        if x.is_alive():
            return True
    return False


if __name__ == '__main__':
    # testing code:
    gen_grid(['debug this phrase, you silly turtle!', 'now debug this one at the same time, if you dare!'], 100, 100)