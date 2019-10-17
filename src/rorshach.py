import random, os, multiprocessing
from factors import factor_combinations
from PIL import Image, ImageFilter
import dual_forces


def gen_grid(phrases, width=480, height=360):
    random.shuffle(phrases)
    for phrase in phrases:
    #
        grid, impressions = dual_forces.darken(phrase, width//2, height)
        print('Phrase:', phrase)
        print('Impressions:', impressions)
        img, smoothed, smoother, smoothest = inkblot(grid, width, height)
        #
        yield img, smoothed, smoother, smoothest, phrase


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