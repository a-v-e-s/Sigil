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
            img, smoothed, smoother, smoothest = inkblot(x[0], x[1], width, height)
            yield img, smoothed, smoother, smoothest, x[2]


def inkblot(grid, inverse, width, height):
    img1 = Image.new('L', (width//2, height), color=255)
    pic1 = img1.load()
    for y in range(img1.size[1]):
        for x in range(img1.size[0]):
            if grid[y][x] == 1:
                pic1[x,y] = 0
            else:
                pic1[x,y] = 255
    img1, pic1 = extend(img1, pic1, 'l')
    #
    img2 = Image.new('L', (width//2, height), color=255)
    pic2 = img2.load()
    for y in range(img2.size[1]):
        for x in range(img2.size[0]):
            if inverse[y][x] == 1:
                pic2[x,y] = 0
            else:
                pic2[x,y] = 255
    img2, pic2 = extend(img2, pic2, 'r')
    #
    img1.show()
    img2.show()
    fusion = Image.new('L', (width, height), color=255)
    fusion.paste(img1)
    fusion.paste(img2, box=(width//2, 0))
    #
    smoothed = fusion.filter(ImageFilter.SMOOTH)
    smoother = fusion.filter(ImageFilter.SMOOTH_MORE)
    smoothest = smoother.filter(ImageFilter.SMOOTH_MORE)
    return fusion, smoothed, smoother, smoothest


def extend(img, pic, lr):
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


if __name__ == '__main__':
    gen_grid(['debug this phrase, you silly turtle!', 'now debug this one at the same time, if you dare!'], 100, 100)