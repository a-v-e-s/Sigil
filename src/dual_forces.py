import random, fibonacci


def darken(phrase, width=256, height=384):
    fib = fibonacci.make_fibonacci(1000)[4:]
    numbs = [ord(x) for x in phrase]
    width = 256
    height = 384
    grid = [[8 for x in range(width)] for x in range(height)]
    inverse = [[8 for x in range(width)] for x in range(height)]
    points = width * height
    pixies = points // 2
    impressions = 0
    #
    # set initial coordinates at random:
    x = random.randint(0, width-1)
    xc = x    # I don't understand why this is necessary but it is.
    y = random.randint(0, height-1)
    zx = width-1 - x
    zy = height-1 - y
    #
    grid[y][x] = 1
    inverse[zy][zx] = 1
    blacks = [(y,x)]
    new_blacks = [True, -1]
    pixies -= 1
    count = 1
    use_first = []
    fail_count = 0
    whitened = False
    #
    # begin the loop!
    #
    while pixies > 0:
        if whitened:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            xc = x
            if grid[y][x] == 8:
                grid[y][x] = 1
                zy = height-1 - y
                zx = width-1 - xc
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
                        zy = height-1 - y
                        zx = width-1 - h
                        inverse[zy][zx] = 1
                        blacks.append((y,h))
                        used = True
                        new_blacks[0] = True
                        new_blacks[1] -= 1
                        pixies -= 1
                        count += 1
                        use_first.remove(b)
                        if pixies == 0:
                            break      
                    if count == fib[0]:
                        fib.remove(count)
                    numbs = numbs[1:] + numbs[:1]
            if y > 0:
                j = y - 1
                if grid[j][xc] != 1 and random.random() <= pixies/points and count != fib[0]:
                    impressions += 1
                    if count % numbs[0] != 0:
                        grid[j][xc] = 1
                        zy = height-1 - j
                        zx = width-1 - xc
                        inverse[zy][zx] = 1
                        blacks.append((j,xc))
                        used = True
                        new_blacks[0] = True
                        new_blacks[1] -= 1
                        pixies -= 1
                        count += 1
                        if b in use_first:
                            use_first.remove(b)
                        if pixies == 0:
                            break
                    if count == fib[0]:
                        fib.remove(count)
                    numbs = numbs[1:] + numbs[:1]
            if y < height-2:
                k = y + 1
                if grid[k][xc] != 1 and random.random() <= pixies/points and count != fib[0]:
                    impressions += 1
                    if count % numbs[0] != 0:
                        grid[k][xc] = 1
                        zy = height-1 - k
                        zx = width-1 - xc
                        inverse[zy][zx] = 1
                        blacks.append((k,xc))
                        used = True
                        new_blacks[0] = True
                        new_blacks[1] -= 1
                        pixies -= 1
                        count += 1
                        if b in use_first:
                            use_first.remove(b)
                        if pixies == 0:
                            break
                    if count == fib[0]:
                        fib.remove(count)
                    numbs = numbs[1:] + numbs[:1]
            if xc < width-2:
                l = xc + 1
                if grid[y][l] != 1 and random.random() <= pixies/points and count != fib[0]:
                    impressions += 1
                    if count % numbs[0] != 0:
                        grid[y][l] = 1
                        zy = height-1 - y
                        zx = width-1 - l
                        inverse[zy][zx] = 1
                        blacks.append((y,l))
                        used = True
                        new_blacks[0] = True
                        new_blacks[1] -= 1
                        pixies -= 1
                        count += 1
                        if b in use_first:
                            use_first.remove(b)
                        if pixies == 0:
                            break
                    if count == fib[0]:
                        fib.remove(count)
                    numbs = numbs[1:] + numbs[:1]
        if used:
            fail_count = 0
            continue
        else:
            fail_count += 1
            if fail_count > len(grid[0]) // 24:
                grid, inverse, width, height, blacks, numbs, pixies, impressions = whiten(grid, inverse, width, height, blacks, numbs, pixies, impressions)
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
                            count += 1
                            grid[y][h] = 1
                            zy = height-1 - y
                            zx = width-1 - h
                            inverse[zy][zx] = 1
                            blacks.append((y,h))
                            new_blacks[0] = True
                            used = True
                            new_blacks[1] -= 1
                            pixies -= 1
                            count += 1
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
                            count += 1
                            grid[j][xc] = 1
                            zy = height-1 - j
                            zx = width-1 - xc
                            inverse[zy][zx] = 1
                            blacks.append((j,xc))
                            new_blacks[0] = True
                            used = True
                            new_blacks[1] -= 1
                            pixies -= 1
                            count += 1
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
                            count += 1
                            grid[k][xc] = 1
                            zy = height-1 - k
                            zx = width-1 - xc
                            inverse[zy][zx] = 1
                            blacks.append((k,xc))
                            new_blacks[0] = True
                            used = True
                            new_blacks[1] -= 1
                            pixies -= 1
                            count += 1
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
                            count += 1
                            grid[y][l] = 1
                            zy = height-1 - y
                            zx = width-1 - l
                            inverse[zy][zx] = 1
                            blacks.append((y,l))
                            new_blacks[0] = True
                            used = True
                            new_blacks[1] -= 1
                            pixies -= 1
                            count += 1
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
                    grid, inverse, width, height, blacks, numbs, pixies, impressions = whiten(grid, inverse, width, height, blacks, numbs, pixies, impressions)
                    use_first = []
                    fail_count = 0
                    whitened = True
    #
    fusion = []
    for x in range(len(grid)):
        combined_line = grid[x] + inverse[x]
        fusion.append(combined_line)
    return fusion, impressions


def whiten(grid, inverse, width, height, blacks, numbs, pixies, impressions):
    fib = fibonacci.make_fibonacci(1000)[4:]
    r = random.choice(blacks)
    y = r[0]
    xc = r[1]
    zy = height-1 - y
    zx = width-1 - xc
    grid[y][xc] = 8
    inverse[zy][zx] = 8
    whites = [(y,xc)]
    new_whites = [True, -1]
    pixies += 1
    use_first = []
    whitening = True
    while whitening:
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
                        zy = height-1 - y
                        zx = width-1 - h
                        inverse[zy][zx] = 8
                        whites.append((y,h))
                        new_whites[0] = True
                        new_whites[1] -= 1
                        whitened += 1
                        pixies += 1
                        blacks.remove((y,h))
                        whitening = True
                        use_first.remove(w)
                    if whitened == fib[0]:
                        fib.remove(whitened)
                    numbs = numbs[1:] + numbs[:1]
            if y > 0:
                j = y - 1
                if grid[j][xc] == 1 and random.random() >= len(whites)/len(blacks) and whitened != fib[0]:
                    impressions += 1
                    if numbs[0] % whitened == 0:
                        grid[j][xc] = 8
                        zy = height-1 - j
                        zx = width-1 - xc
                        inverse[zy][zx] = 8
                        whites.append((j,xc))
                        new_whites[0] = True
                        new_whites[1] -= 1
                        whitened += 1
                        pixies += 1
                        blacks.remove((j,xc))
                        whitening = True
                        if w in use_first:
                            use_first.remove(w)
                    if whitened == fib[0]:
                        fib.remove(whitened)
                    numbs = numbs[1:] + numbs[:1]
            if y < height-2:
                k = y + 1
                if grid[k][xc] == 1 and random.random() >= len(whites)/len(blacks) and whitened != fib[0]:
                    impressions += 1
                    if numbs[0] % whitened == 0:
                        grid[k][xc] = 8
                        zy = height-1 - k
                        zx = width-1 - xc
                        inverse[zy][zx] = 8
                        whites.append((k,xc))
                        new_whites[0] = True
                        new_whites[1] -= 1
                        whitened += 1
                        pixies += 1
                        blacks.remove((k,xc))
                        whitening = True
                        if w in use_first:
                            use_first.remove(w)
                    if whitened == fib[0]:
                        fib.remove(whitened)
                    numbs = numbs[1:] + numbs[:1]
            if xc < width-2:
                l = xc + 1
                if grid[y][l] == 1 and random.random() >= len(whites)/len(blacks) and whitened != fib[0]:
                    impressions += 1
                    if numbs[0] % whitened == 0:
                        grid[y][l] = 8
                        zy = height-1 - y
                        zx = width-1 - l
                        inverse[zy][zx] = 8
                        whites.append((y,l))
                        new_whites[0] = True
                        new_whites[1] -= 1
                        whitened += 1
                        pixies += 1
                        blacks.remove((y,l))
                        whitening = True
                        if w in use_first:
                            use_first.remove(w)
                    if whitened == fib[0]:
                        fib.remove(whitened)
                    numbs = numbs[1:] + numbs[:1]
    #
    return grid, inverse, width, height, blacks, numbs, pixies, impressions


if __name__ == '__main__':
    grid, inverse, impressions = darken(phrase='debug this nonsense, you turtle fucker.')