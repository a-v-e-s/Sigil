#!/usr/bin/trip_the_F_out

import random, pickle, fibonacci, colorsys

# Define some important constants:
fib = fibonacci.make_fibonacci(1000)[4:]
#
hue_shift = random.uniform(-0.25, 0.25)
lightness = 0.5
saturation = 0.9
#
variation = 0.125
base_A = 0.25
base_B = 0.75
lower_A = base_A - variation
upper_A = base_A + variation
lower_B = base_B - variation
upper_B = base_B + variation
#
fail_out = 36 # this should probably be done a little differently.
switch_const = 0.16 # 0.08
shft_dgr = 0.003 # 0.01
n_shft_dgr = 1 - shft_dgr
#
relatives = {
    'z': 0.00077,
    'q': 0.00095,
    'x': 0.0015,
    'j': 0.00153,
    'v': 0.00978,
    'k': 0.01292,
    'b': 0.01492,
    'p': 0.01929,
    'y': 0.01994,
    'g': 0.02015,
    'c': 0.02202,
    'f': 0.02228,
    'm': 0.02406,
    'w': 0.0256,
    'u': 0.02758,
    'l': 0.04025,
    'd': 0.04253,
    'r': 0.05987,
    'h': 0.06094,
    's': 0.06327,
    'n': 0.06749,
    'i': 0.06966,
    'o': 0.07507,
    'a': 0.08167,
    't': 0.09356,
    'e': 0.12702
}
#
shift_denominator = relatives['e']
switch_numerator = relatives['z']


def switch_prob(key):
    try:
        # experiment with different values for the constant here:
        return ((switch_numerator / relatives[key]) * switch_const)
    except KeyError:
        return 0


def switch(rising, key):
    if random.random() < switch_prob(key):
        if rising == True:
            rising = False
        else:
            rising = True
    return rising


def shift_prob(key):
    # this is probably returning values that are too high on average,
    # causing shift to shift too little...
    try:
        return (relatives[key] / shift_denominator)
    except KeyError:
        return 0


def shift(rising, upper, lower, key, val, impressions):
    impressions += 1
    if random.random() < shift_prob(key):
        if rising:
            if (val + shft_dgr) <= upper:
                if (val + shft_dgr) <= 1:
                    return val + shft_dgr
                else:
                    return val - n_shft_dgr
            else:
                rising = False
                if (val - shft_dgr) >= 0:
                    return val - shft_dgr
                else:
                    return val + n_shft_dgr
        else:
            if (val - shft_dgr) >= lower:
                if (val - shft_dgr) >= 0:
                    return val - shft_dgr
                else:
                    return val + n_shft_dgr
            else:
                rising = True
                if (val + shft_dgr) <= 1:
                    return val + shft_dgr
                else:
                    return val - n_shft_dgr
    else:
        return val
    

def colour(phrase, progress, width=100, height=100):
    original_phrase = phrase
    rising = random.choice([True, False])
    codename = hex(hash(phrase))[2:]
    numbs = [ord(x) for x in phrase]
    grid = [[base_A for x in range(width)] for x in range(height)]
    points = width * height
    pixies = points // 2
    impressions = 0
    # set initial coordinates at random:
    x = random.randint(0, width-1)
    xc = x    # I don't understand why this is necessary but it is.
    y = random.randint(0, height-1)
    #
    grid[y][x] = random.uniform(0.5, 1)
    Bs = [(y,x)]
    new_Bs = [True, -1]
    pixies -= 1
    count = 1
    use_first = []
    fail_count = 0
    inverted = False
    #
    # begin the loop!
    while pixies > 0:
        try:
            progress[codename] = impressions
        except Exception:
            pass
        if inverted:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            xc = x
            if upper_A >= grid[y][x] >= lower_A:
                # make this more random:
                grid[y][x] = random.uniform(0.5, 1)
                pixies -= 1
                count += 1
                Bs.append((y,xc))
                use_first.append((y,xc))
                new_Bs = [True, -1]
                inverted = False
            else:
                continue
        elif new_Bs[0] == True:
            for a in range(-1, (new_Bs[1] - 1), -1):
                use_first.append(Bs[a])
            new_Bs = [False, 0]
            used = False
        for b in use_first:
            y = b[0]
            xc = b[1]
            if xc > 0:
                h = xc - 1
                if grid[y][h] < 0.5 and random.random() <= pixies/points and count != fib[0]:
                    impressions += 1
                    if count % numbs[0] != 0:
                        grid[y][h] = shift(rising, upper_B, lower_B, phrase[0], grid[b[0]][b[1]], impressions)
                        rising = switch(rising, phrase[0])
                        count += 1
                        pixies -= 1
                        used = True
                        Bs.append((y,h))
                        new_Bs[0] = True
                        new_Bs[1] -= 1
                        use_first.remove(b)
                        if pixies == 0:
                            break      
                    numbs = numbs[1:] + numbs[:1]
                    phrase = phrase[1:] + phrase[:1]
                if count == fib[0]:
                    fib.remove(count)
            if y > 0:
                j = y - 1
                if grid[j][xc] < 0.5 and random.random() <= pixies/points and count != fib[0]:
                    impressions += 1
                    if count % numbs[0] != 0:
                        grid[j][xc] = shift(rising, upper_B, lower_B, phrase[0], grid[b[0]][b[1]], impressions)
                        rising = switch(rising, phrase[0])
                        count += 1
                        pixies -= 1
                        used = True
                        Bs.append((j,xc))
                        new_Bs[0] = True
                        new_Bs[1] -= 1
                        if b in use_first:
                            use_first.remove(b)
                        if pixies == 0:
                            break
                    numbs = numbs[1:] + numbs[:1]
                    phrase = phrase[1:] + phrase[:1]
                if count == fib[0]:
                    fib.remove(count)
            if y < height-1:
                k = y + 1
                if grid[k][xc] < 0.5 and random.random() <= pixies/points and count != fib[0]:
                    impressions += 1
                    if count % numbs[0] != 0:
                        grid[k][xc] = shift(rising, upper_B, lower_B, phrase[0], grid[b[0]][b[1]], impressions)
                        rising = switch(rising, phrase[0])
                        count += 1
                        pixies -= 1
                        used = True
                        Bs.append((k,xc))
                        new_Bs[0] = True
                        new_Bs[1] -= 1
                        if b in use_first:
                            use_first.remove(b)
                        if pixies == 0:
                            break
                    numbs = numbs[1:] + numbs[:1]
                    phrase = phrase[1:] + phrase[:1]
                if count == fib[0]:
                    fib.remove(count)
            if xc < width-1:
                l = xc + 1
                if grid[y][l] < 0.5 and random.random() <= pixies/points and count != fib[0]:
                    impressions += 1
                    if count % numbs[0] != 0:
                        grid[y][l] = shift(rising, upper_B, lower_B, phrase[0], grid[b[0]][b[1]], impressions)
                        rising = switch(rising, phrase[0])
                        count += 1
                        pixies -= 1
                        used = True
                        Bs.append((y,l))
                        new_Bs[0] = True
                        new_Bs[1] -= 1
                        if b in use_first:
                            use_first.remove(b)
                        if pixies == 0:
                            break
                    numbs = numbs[1:] + numbs[:1]
                    phrase = phrase[1:] + phrase[:1]
                if count == fib[0]:
                    fib.remove(count)
        if used:
            fail_count = 0
            continue
        else:
            fail_count += 1
            if fail_count > len(grid[0]) // fail_out:
                (
                    grid,
                    width,
                    height,
                    phrase,
                    Bs,
                    numbs,
                    pixies,
                    progress,
                    codename,
                    impressions
                ) = invert(
                    grid,
                    width,
                    height,
                    phrase,
                    Bs,
                    numbs,
                    pixies,
                    progress,
                    codename,
                    impressions
                )
                use_first = []
                fail_count = 0
                inverted = True
                continue
            Bs.reverse()
            for c in Bs:
                y = c[0]
                xc = c[1]
                if xc > 0:
                    h = xc - 1
                    if grid[y][h] < 0.5 and random.random() <= pixies/points and count != fib[0]:
                        impressions += 1
                        if count % numbs[0] != 0:
                            grid[y][h] = shift(rising, upper_B, lower_B, phrase[0], grid[c[0]][c[1]], impressions)
                            rising = switch(rising, phrase[0])
                            count += 1
                            pixies -= 1
                            used = True
                            Bs.append((y,h))
                            new_Bs[0] = True
                            new_Bs[1] -= 1
                            numbs = numbs[1:] + numbs[:1]
                            phrase = phrase[1:] + phrase[:1]
                            if pixies == 0:
                                break
                    if count == fib[0]:
                        fib.remove(count)
                if y > 0:
                    j = y - 1
                    if grid[j][xc] < 0.5 and random.random() <= pixies/points and count != fib[0]:
                        impressions += 1
                        if count % numbs[0] != 0:
                            grid[j][xc] = shift(rising, upper_B, lower_B, phrase[0], grid[c[0]][c[1]], impressions)
                            rising = switch(rising, phrase[0])
                            count += 1
                            pixies -= 1
                            used = True
                            Bs.append((j,xc))
                            new_Bs[0] = True
                            new_Bs[1] -= 1
                            numbs = numbs[1:] + numbs[:1]
                            phrase = phrase[1:] + phrase[:1]
                            if pixies == 0:
                                break
                    if count == fib[0]:
                        fib.remove(count)
                if y < height-1:
                    k = y + 1
                    if grid[k][xc] < 0.5 and random.random() <= pixies/points and count != fib[0]:
                        impressions += 1
                        if count % numbs[0] != 0:
                            grid[k][xc] = shift(rising, upper_B, lower_B, phrase[0], grid[c[0]][c[1]], impressions)
                            rising = switch(rising, phrase[0])
                            count += 1
                            pixies -= 1
                            used = True
                            Bs.append((k,xc))
                            new_Bs[0] = True
                            new_Bs[1] -= 1
                            numbs = numbs[1:] + numbs[:1]
                            phrase = phrase[1:] + phrase[:1]
                            if pixies == 0:
                                break
                    if count == fib[0]:
                        fib.remove(count)
                if xc < width-1:
                    l = xc + 1
                    if grid[y][l] < 0.5 and random.random() <= pixies/points and count != fib[0]:
                        impressions += 1
                        if count % numbs[0] != 0:
                            grid[y][l] = shift(rising, upper_B, lower_B, phrase[0], grid[c[0]][c[1]], impressions)
                            rising = switch(rising, phrase[0])
                            count += 1
                            pixies -= 1
                            used = True
                            Bs.append((y,l))
                            new_Bs[0] = True
                            new_Bs[1] -= 1
                            numbs = numbs[1:] + numbs[:1]
                            phrase = phrase[1:] + phrase[:1]
                            if pixies == 0:
                                break
                    if count == fib[0]:
                        fib.remove(count)
                if used:
                    fail_count = 0
                    Bs.reverse()
                    break
            if not used:
                fail_count += 1
                Bs.reverse()
                if fail_count > len(grid[0]) // fail_out:
                    (
                        grid,
                        width,
                        height,
                        phrase,
                        Bs,
                        numbs,
                        pixies,
                        progress,
                        codename,
                        impressions
                    ) = invert(
                        grid,
                        width,
                        height,
                        phrase,
                        Bs,
                        numbs,
                        pixies,
                        progress,
                        codename,
                        impressions
                    )
                    use_first = []
                    fail_count = 0
                    inverted = True
    #
    # create the inverse grid:
    #inverse = [[8 for x in range(width)] for x in range(height)]
    #rownum = -1
    #for row in grid:
    #    rownum += 1
    #    colnum = -1
    #    for x in row:
    #        colnum += 1
    #        if x == 1:
    #            inverse[(len(grid)-1 - rownum)][(len(row)-1 - colnum)] = 1
    #
    rownum = -1
    for row in grid:
        rownum += 1
        colnum = -1
        for x in row:
            colnum += 1
            x += hue_shift
            if x > 1:
                x -= 1
            if x < 0:
                x += 1
            grid[rownum][colnum] = [round((255 * c)) for c in colorsys.hls_to_rgb(x, lightness, saturation)]
    #
    # return if testing:
    if original_phrase == 'turtle clucker.':
        return grid, impressions
    # save to grids pickle file if not testing:
    # final impression count:
    try:
        progress[codename] = impressions
    except Exception:
        pass
    try:
        with open('grids.pkl', 'rb') as f:
            grids = pickle.load(f)
        grids.append((grid, phrase))
        with open('grids.pkl', 'wb') as f:
            pickle.dump(grids, f)
    except (EOFError, FileNotFoundError):
        grids = []
        grids.append((grid, phrase))
        with open('grids.pkl', 'wb') as f:
            pickle.dump(grids, f)


def invert(grid, width, height, phrase, Bs, numbs, pixies, progress, codename, impressions):
    rising = random.choice([True, False])
    #r = random.choice(Bs)
    y = random.choice(range(height))
    xc = random.choice(range(width))
    grid[y][xc] = random.uniform(0, 0.5)
    As = [(y,xc)]
    new_As = [True, -1]
    pixies += 1
    use_first = []
    inverting = True
    while inverting:
        try:
            progress[codename] = impressions
        except Exception:
            pass
        inverting = False
        for a in range(-1, (new_As[1] - 1), -1):
            use_first.append(As[a])
        new_As = [False, 0]
        for w in use_first:
            inverted = 1
            y = w[0]
            xc = w[1]
            if xc > 0:
                h = xc - 1
                if grid[y][h] > 0.5 and random.random() >= len(As)/len(Bs) and inverted != fib[0]:
                    impressions += 1
                    if numbs[0] % inverted == 0:
                        grid[y][h] = shift(rising, upper_A, lower_A, phrase[0], grid[w[0]][w[1]], impressions)
                        rising = switch(rising, phrase[0])
                        inverting = True
                        inverted += 1
                        pixies += 1
                        As.append((y,h))
                        new_As[0] = True
                        new_As[1] -= 1
                        Bs.remove((y,h))
                        use_first.remove(w)
                    numbs = numbs[1:] + numbs[:1]
                    phrase = phrase[1:] + phrase[:1]
                if inverted == fib[0]:
                    fib.remove(inverted)
            if y > 0:
                j = y - 1
                if grid[j][xc] > 0.5 and random.random() >= len(As)/len(Bs) and inverted != fib[0]:
                    impressions += 1
                    if numbs[0] % inverted == 0:
                        grid[j][xc] = shift(rising, upper_A, lower_A, phrase[0], grid[w[0]][w[1]], impressions)
                        rising = switch(rising, phrase[0])
                        inverting = True
                        inverted += 1
                        pixies += 1
                        As.append((j,xc))
                        new_As[0] = True
                        new_As[1] -= 1
                        Bs.remove((j,xc))
                        if w in use_first:
                            use_first.remove(w)
                    numbs = numbs[1:] + numbs[:1]
                    phrase = phrase[1:] + phrase[:1]
                if inverted == fib[0]:
                    fib.remove(inverted)
            if y < height-1:
                k = y + 1
                if grid[k][xc] > 0.5 and random.random() >= len(As)/len(Bs) and inverted != fib[0]:
                    impressions += 1
                    if numbs[0] % inverted == 0:
                        grid[k][xc] = shift(rising, upper_A, lower_A, phrase[0], grid[w[0]][w[1]], impressions)
                        rising = switch(rising, phrase[0])
                        inverting = True
                        inverted += 1
                        pixies += 1
                        As.append((k,xc))
                        new_As[0] = True
                        new_As[1] -= 1
                        Bs.remove((k,xc))
                        if w in use_first:
                            use_first.remove(w)
                    numbs = numbs[1:] + numbs[:1]
                    phrase = phrase[1:] + phrase[:1]
                if inverted == fib[0]:
                    fib.remove(inverted)
            if xc < width-1:
                l = xc + 1
                if grid[y][l] > 0.5 and random.random() >= len(As)/len(Bs) and inverted != fib[0]:
                    impressions += 1
                    if numbs[0] % inverted == 0:
                        grid[y][l] = shift(rising, upper_A, lower_A, phrase[0], grid[w[0]][w[1]], impressions)
                        rising = switch(rising, phrase[0])
                        inverting = True
                        inverted += 1
                        pixies += 1
                        As.append((y,l))
                        new_As[0] = True
                        new_As[1] -= 1
                        Bs.remove((y,l))
                        if w in use_first:
                            use_first.remove(w)
                    numbs = numbs[1:] + numbs[:1]
                    phrase = phrase[1:] + phrase[:1]
                if inverted == fib[0]:
                    fib.remove(inverted)
    #
    return grid, width, height, phrase, Bs, numbs, pixies, progress, codename, impressions


if __name__ == '__main__':
    # testing code:
    from PIL import Image
    phrase = 'turtle clucker.'
    width, height = 200, 200
    grid, impressions = colour(phrase, {hex(hash(phrase))[2:]: 0}, width, height)
    #
    print('impressions:', impressions)
    image = Image.new('RGB', (width, height), color=(0, 0, 0))
    pic1 = image.load()
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            pic1[x,y] = tuple(grid[y][x])
    image.show()