import random, os, multiprocessing, pickle
from factors import factor_combinations
from PIL import Image, ImageFilter
import dual_forces


def gen_grid(phrases, width=480, height=360):
    random.shuffle(phrases)
    processors = multiprocessing.cpu_count()
    #
    jobs = []
    for phrase in phrases:
        p = multiprocessing.Process(target=dual_forces.darken, args=(phrase, width//2, height))
        jobs.append(p)
    if len(jobs) >= processors:
        print('Dividing up the jobs')
        while jobs:
            do_these = jobs[:processors-1]
            for x in do_these:
                x.start()
                print('started:', x)
            for x in do_these:
                x.join()
                print('joined:', x)
            jobs = jobs[processors-1:]
    else:
        for x in jobs:
            x.start()
            print('started:', x)
        for x in jobs:
            x.join()
            print('joined:', x)
    #print('Phrase:', phrase)
    #print('Impressions:', impressions)
    with open('grids.pkl', 'rb') as f:
        grids = pickle.load(f)
        for x in grids:
            img, smoothed, smoother, smoothest = inkblot(x[0], width, height)
            yield img, smoothed, smoother, smoothest, x[1]


def inkblot(grid, width, height):
    img = Image.new('L', (width, height), color=255)
    pic = img.load()
    #
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if grid[y][x] == 1:
                pic[x,y] = 0
            else:
                pic[x,y] = 255
    #
    smoothed = img.filter(ImageFilter.SMOOTH)
    smoother = img.filter(ImageFilter.SMOOTH_MORE)
    smoothest = smoother.filter(ImageFilter.SMOOTH_MORE)
    return img, smoothed, smoother, smoothest


if __name__ == '__main__':
    gen_grid(['debug this phrase, you silly turtle!', 'now debug this one at the same time, if you dare!'], 100, 100)