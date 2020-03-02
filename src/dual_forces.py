"""
dual_forces.py: Where all the magic really happens.

The darken function turns values in the grid and inverse lists from 8 to 1, indicating that the corresponding pixel in the encoded image will be black.
The whiten function turns values in the grid and inverse lists from 1 to 8, indicating that the corresponding pixel in the encoded image will be white.
The process continues indefinitely until half of all the pixels will be turned black, and half will be white. 

Following is a description of the purpose of most of the variables in use:

phrase: user supplied data to be randomly encoded into an image
codename: obfuscated hash of the phrase
fib: sequence of the first 1000 fibonacci numbers; used to determine whether or not to fill in a grid point.
numbs: formed from phrase and used to determine whether or not to fill in a grid point
grid : array of grid points used to determine whether to fill in pixels on an image
points: total grid points in one of the two grids
pixies: total grid points which will be darkened in one of the two grids
impressions: number oftimes time phrase is used to encode itself into the image
xc: coordinates for main grid
y: coordinates for main grid
blacks: list of all grid points to be shaded black
new_blacks: [whether or not new grid points were darkened on previous while loop, and how many]
count: total number of grid points darkened. never resets. removed from fib when count == fib[0]. not used in whiten method
use_first: darkened grid points whom have not yet been expanded out from, to be given the first chance to be expanded out from.
fail_count: how many times the 2 major for loops in the darken function have been iterated through. if it exceeds len(grid[0]) // 24 then the whiten function is called and it is then reset.
whitened: set after the whiten function is finished and used near the beginning of the while loop to determine whether to choose a random, new starting point for darkening, then reset to False.
progress: dictionary used for interprocess communication to send the number of impressions at the beginning of each while loop
r: a darkened grid point, chosen at random, to turn light and expand outwards from
whites: list of tupled coordinates of each grid point turned white during the function call
new_whites: [whether or not any grid points were whitened during the previous while loop, and how many]
whitening: whether any grid points were whitened on this iteration of the while loop. if false the while loop exits and the function returns
whitened: used to decide whether or not to whiten a given grid point. if whitened == fib[0] then that value is removed from fib. the whiten functions corollary to count.

I hope that helps anyone masochistic enough to try and untangle this mess.
"""

import random, pickle, fibonacci


def darken(phrase, progress, width=240, height=360):
    codename = hex(hash(phrase))[2:]
    fib = fibonacci.make_fibonacci(1000)[4:]
    numbs = [ord(x) for x in phrase]
    grid = [[8 for x in range(width)] for x in range(height)]
    points = width * height
    pixies = points // 2
    impressions = 0
    #
    # set initial coordinates at random:
    x = random.randint(0, width-1)
    xc = x    # I don't understand why this is necessary but it is.
    y = random.randint(0, height-1)
    #
    grid[y][x] = 1
    blacks = [(y,x)]
    new_blacks = [True, -1]
    pixies -= 1
    count = 1
    use_first = []
    fail_count = 0
    whitened = False
    #
    # begin the loop!
    while pixies > 0:
        try:
            progress[codename] = impressions
        except Exception:
            pass
        if whitened:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            xc = x
            if grid[y][x] == 8:
                grid[y][x] = 1
                pixies -= 1
                count += 1
                blacks.append((y,xc))
                use_first.append((y,xc))
                new_blacks = [True, -1]
                whitened = False
            else:
                continue
        elif new_blacks[0] == True:
            for a in range(-1, (new_blacks[1] - 1), -1):
                use_first.append(blacks[a])
            new_blacks = [False, 0]
            used = False
        for b in use_first:
            y = b[0]
            xc = b[1]
            if xc > 0:
                h = xc - 1
                if grid[y][h] != 1 and random.random() <= pixies/points and count != fib[0]:
                    impressions += 1
                    if count % numbs[0] != 0:
                        grid[y][h] = 1
                        count += 1
                        pixies -= 1
                        used = True
                        blacks.append((y,h))
                        new_blacks[0] = True
                        new_blacks[1] -= 1
                        use_first.remove(b)
                        if pixies == 0:
                            break      
                    numbs = numbs[1:] + numbs[:1]
                if count == fib[0]:
                    fib.remove(count)
            if y > 0:
                j = y - 1
                if grid[j][xc] != 1 and random.random() <= pixies/points and count != fib[0]:
                    impressions += 1
                    if count % numbs[0] != 0:
                        grid[j][xc] = 1
                        count += 1
                        pixies -= 1
                        used = True
                        blacks.append((j,xc))
                        new_blacks[0] = True
                        new_blacks[1] -= 1
                        if b in use_first:
                            use_first.remove(b)
                        if pixies == 0:
                            break
                    numbs = numbs[1:] + numbs[:1]
                if count == fib[0]:
                    fib.remove(count)
            if y < height-2:
                k = y + 1
                if grid[k][xc] != 1 and random.random() <= pixies/points and count != fib[0]:
                    impressions += 1
                    if count % numbs[0] != 0:
                        grid[k][xc] = 1
                        count += 1
                        pixies -= 1
                        used = True
                        blacks.append((k,xc))
                        new_blacks[0] = True
                        new_blacks[1] -= 1
                        if b in use_first:
                            use_first.remove(b)
                        if pixies == 0:
                            break
                    numbs = numbs[1:] + numbs[:1]
                if count == fib[0]:
                    fib.remove(count)
            if xc < width-2:
                l = xc + 1
                if grid[y][l] != 1 and random.random() <= pixies/points and count != fib[0]:
                    impressions += 1
                    if count % numbs[0] != 0:
                        grid[y][l] = 1
                        count += 1
                        pixies -= 1
                        used = True
                        blacks.append((y,l))
                        new_blacks[0] = True
                        new_blacks[1] -= 1
                        if b in use_first:
                            use_first.remove(b)
                        if pixies == 0:
                            break
                    numbs = numbs[1:] + numbs[:1]
                if count == fib[0]:
                    fib.remove(count)
        if used:
            fail_count = 0
            continue
        else:
            fail_count += 1
            if fail_count > len(grid[0]) // 24:
                grid, width, height, blacks, numbs, pixies, progress, codename, impressions = whiten(grid, width, height, blacks, numbs, pixies, progress, codename, impressions)
                use_first = []
                fail_count = 0
                whitened = True
                continue
            blacks.reverse()
            for c in blacks:
                y = c[0]
                xc = c[1]
                if xc > 0:
                    h = xc - 1
                    if grid[y][h] != 1 and random.random() <= pixies/points and count != fib[0]:
                        impressions += 1
                        if count % numbs[0] != 0:
                            grid[y][h] = 1
                            count += 1
                            pixies -= 1
                            used = True
                            blacks.append((y,h))
                            new_blacks[0] = True
                            new_blacks[1] -= 1
                            numbs = numbs[1:] + numbs[:1]
                            if pixies == 0:
                                break
                    if count == fib[0]:
                        fib.remove(count)
                if y > 0:
                    j = y - 1
                    if grid[j][xc] != 1 and random.random() <= pixies/points and count != fib[0]:
                        impressions += 1
                        if count % numbs[0] != 0:
                            grid[j][xc] = 1
                            count += 1
                            pixies -= 1
                            used = True
                            blacks.append((j,xc))
                            new_blacks[0] = True
                            new_blacks[1] -= 1
                            numbs = numbs[1:] + numbs[:1]
                            if pixies == 0:
                                break
                    if count == fib[0]:
                        fib.remove(count)
                if y < height-2:
                    k = y + 1
                    if grid[k][xc] != 1 and random.random() <= pixies/points and count != fib[0]:
                        impressions += 1
                        if count % numbs[0] != 0:
                            grid[k][xc] = 1
                            count += 1
                            pixies -= 1
                            used = True
                            blacks.append((k,xc))
                            new_blacks[0] = True
                            new_blacks[1] -= 1
                            numbs = numbs[1:] + numbs[:1]
                            if pixies == 0:
                                break
                    if count == fib[0]:
                        fib.remove(count)
                if xc < width-2:
                    l = xc + 1
                    if grid[y][l] != 1 and random.random() <= pixies/points and count != fib[0]:
                        impressions += 1
                        if count % numbs[0] != 0:
                            grid[y][l] = 1
                            count += 1
                            pixies -= 1
                            used = True
                            blacks.append((y,l))
                            new_blacks[0] = True
                            new_blacks[1] -= 1
                            numbs = numbs[1:] + numbs[:1]
                            if pixies == 0:
                                break
                    if count == fib[0]:
                        fib.remove(count)
                if used:
                    fail_count = 0
                    blacks.reverse()
                    break
            if not used:
                fail_count += 1
                blacks.reverse()
                if fail_count > len(grid[0]) // 24:
                    grid, width, height, blacks, numbs, pixies, progress, codename, impressions = whiten(grid, width, height, blacks, numbs, pixies, progress, codename, impressions)
                    use_first = []
                    fail_count = 0
                    whitened = True
    #
    # create the inverse grid:
    inverse = [[8 for x in range(width)] for x in range(height)]
    rownum = -1
    for row in grid:
        rownum += 1
        colnum = -1
        for x in row:
            colnum += 1
            if x == 1:
                inverse[(len(grid)-1 - rownum)][(len(row)-1 - colnum)] = 1
    #
    # return if testing:
    if phrase == 'turtle clucker.':
        return grid, inverse, impressions
    # final impression count:
    try:
        progress[codename] = impressions
    except Exception:
        pass
    #
    # save to grids pickle file if not testing:
    # probably a slight chance of race conditions here :S
    save_this = (grid, inverse, phrase, impressions)
    try:
        with open('grids.pkl', 'rb') as f:
            grids = pickle.load(f)
        grids.append(save_this)
        with open('grids.pkl', 'wb') as f:
            pickle.dump(grids, f)
    except (EOFError, FileNotFoundError):
        grids = []
        grids.append(save_this)
        with open('grids.pkl', 'wb') as f:
            pickle.dump(grids, f)


def whiten(grid, width, height, blacks, numbs, pixies, progress, codename, impressions):
    fib = fibonacci.make_fibonacci(1000)[4:]
    r = random.choice(blacks)
    y = r[0]
    xc = r[1]
    grid[y][xc] = 8
    whites = [(y,xc)]
    new_whites = [True, -1]
    pixies += 1
    use_first = []
    whitening = True
    while whitening:
        try:
            progress[codename] = impressions
        except Exception:
            pass
        whitening = False
        for a in range(-1, (new_whites[1] - 1), -1):
            use_first.append(whites[a])
        new_whites = [False, 0]
        for w in use_first:
            whitened = 1
            y = w[0]
            xc = w[1]
            if xc > 0:
                h = xc - 1
                if grid[y][h] == 1 and random.random() >= len(whites)/len(blacks) and whitened != fib[0]:
                    impressions += 1
                    if numbs[0] % whitened == 0:
                        grid[y][h] = 8
                        whitening = True
                        whitened += 1
                        pixies += 1
                        whites.append((y,h))
                        new_whites[0] = True
                        new_whites[1] -= 1
                        blacks.remove((y,h))
                        use_first.remove(w)
                    numbs = numbs[1:] + numbs[:1]
                if whitened == fib[0]:
                    fib.remove(whitened)
            if y > 0:
                j = y - 1
                if grid[j][xc] == 1 and random.random() >= len(whites)/len(blacks) and whitened != fib[0]:
                    impressions += 1
                    if numbs[0] % whitened == 0:
                        grid[j][xc] = 8
                        whitening = True
                        whitened += 1
                        pixies += 1
                        whites.append((j,xc))
                        new_whites[0] = True
                        new_whites[1] -= 1
                        blacks.remove((j,xc))
                        if w in use_first:
                            use_first.remove(w)
                    numbs = numbs[1:] + numbs[:1]
                if whitened == fib[0]:
                    fib.remove(whitened)
            if y < height-2:
                k = y + 1
                if grid[k][xc] == 1 and random.random() >= len(whites)/len(blacks) and whitened != fib[0]:
                    impressions += 1
                    if numbs[0] % whitened == 0:
                        grid[k][xc] = 8
                        whitening = True
                        whitened += 1
                        pixies += 1
                        whites.append((k,xc))
                        new_whites[0] = True
                        new_whites[1] -= 1
                        blacks.remove((k,xc))
                        if w in use_first:
                            use_first.remove(w)
                    numbs = numbs[1:] + numbs[:1]
                if whitened == fib[0]:
                    fib.remove(whitened)
            if xc < width-2:
                l = xc + 1
                if grid[y][l] == 1 and random.random() >= len(whites)/len(blacks) and whitened != fib[0]:
                    impressions += 1
                    if numbs[0] % whitened == 0:
                        grid[y][l] = 8
                        whitening = True
                        whitened += 1
                        pixies += 1
                        whites.append((y,l))
                        new_whites[0] = True
                        new_whites[1] -= 1
                        blacks.remove((y,l))
                        if w in use_first:
                            use_first.remove(w)
                    numbs = numbs[1:] + numbs[:1]
                if whitened == fib[0]:
                    fib.remove(whitened)
    #
    return grid, width, height, blacks, numbs, pixies, progress, codename, impressions


if __name__ == '__main__':
    # testing code:
    from PIL import Image
    phrase = 'turtle clucker.'
    width, height = 200, 200
    grid, inverse, impressions = darken(phrase, {hex(hash(phrase))[2:]: 0}, width, height)
    #
    print('impressions:', impressions)
    print('fibonacci numbers left / 1000:', len(fib))
    image = Image.new('L', (width, height))
    pic1 = image.load()
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if grid[y][x] == 8:
                pic1[x,y] = 255
            else:
                pic1[x,y] = 0
    image.show()