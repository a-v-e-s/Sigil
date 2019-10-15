import random, os, multiprocessing
from factors import factor_combinations
from PIL import Image, ImageFilter
import dual_forces


def inkblot(phrases, width=1024, height=768):
    random.shuffle(phrases)
    s_width = width / 4
    s_height = height / 2
    for phrase in phrases:
    #
        p = multiprocessing.Process(target=dual_forces.darken, args=(phrase, s_width, s_height))
        grid, impressions = p.start()
        #
        print('Impressions:', impressions)
        #
        img = Image.new('L', (width, height), color=255)
        pic = img.load()
        #
        x = -1
        y = -1
        for row in grid:
            y += 1
            if y == height:
                break
            for pixel in row:
                x += 1
                if x == width:
                    x = -1
                    break
                if pixel == 1:
                    pic[x,y] = 0
        #
        img.show()


if __name__ == '__main__':
    inkblot(['debug this phrase, you silly turtle!', 'now debug this one at the same time, if you dare!'], 100, 100)