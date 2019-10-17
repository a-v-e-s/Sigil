from PIL import Image, ImageFont, ImageDraw, ImageOps
import os, random, chaos, math
import fibonacci

fib = fibonacci.make_fibonacci(1000)[4:]
alphabet = {
    'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,
    'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26
}


def rotate(lisp):
    lisp = lisp[1:] + lisp[:1]
    return lisp


def list_pixels(phrase):
    font_options = []
    for x in os.listdir('fonts'):
        font_options.append(os.path.join(os.getcwd(), 'fonts', x))

    font = ImageFont.truetype(font=random.choice(font_options), size=48, encoding='unic')
    text_width, text_height = font.getsize(phrase)
    canvas = Image.new('L', (text_width, text_height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((0, 0), phrase, 'black', font)
    pixels = canvas.getdata()
    return list(pixels)

def text_img(phrase):
    font_options = []
    for x in os.listdir('fonts'):
        font_options.append(os.path.join(os.getcwd(), 'fonts', x))

    font = ImageFont.truetype(font=random.choice(font_options), size=48, encoding='unic')
    text_width, text_height = font.getsize(phrase)
    canvas = Image.new('L', (text_width, text_height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((0, 0), phrase, 'black', font)
    canvas.show()

def regrid(width=24, height=30, pixies=0):
    # x, xc, y, grid, pixies = regrid()
    if pixies == 0:
        pixies = width * height / 3
    grid = [[0 for x in range(width)] for x in range(height)]
    x = random.randint(0, width-1)
    xc = x
    y = random.randint(0, height-1)
    grid[y][x] = 1
    # x is now a list for some reason so beware...
    return x, xc, y, grid, pixies


def grid0(width=24, height=30, pixies=0):
    points = width * height
    if pixies == 0:
        pixies = points // 3
    grid = [[0 for x in range(width)] for x in range(height)]
    x = random.randint(0, width-1)
    xc = x
    y = random.randint(0, height-1)
    #
    grid[y][x] = 1
    blacks = [(y,x)]
    new_blacks = [True, -1]
    pixies -= 1
    #
    # x may now be a list for some reason so beware...
    #
    use_these = []
    while pixies > 0:
        if new_blacks[0] == True:
            for a in range(-1, (new_blacks[1] - 1), -1):
                use_these.append(blacks[a])
            new_blacks = [False, 0]
            used = False
        for b in use_these:
            y = b[0]
            xc = b[1]
            if xc > 0:
                h = xc - 1
                if grid[y][h] != 1 and random.random() <= pixies/points:
                    grid[y][h] = 1
                    blacks.append((y,h))
                    used = True
                    new_blacks[0] = True
                    new_blacks[1] -= 1
                    pixies -= 1
            if y > 0:
                j = y - 1
                if grid[j][xc] != 1 and random.random() <= pixies/points:
                    grid[j][xc] = 1
                    blacks.append((j,xc))
                    used = True
                    new_blacks[0] = True
                    new_blacks[1] -= 1
                    pixies -= 1
            if y < height-2:
                k = y + 1
                if grid[k][xc] != 1 and random.random() <= pixies/points:
                    grid[k][xc] = 1
                    blacks.append((k,xc))
                    used = True
                    new_blacks[0] = True
                    new_blacks[1] -= 1
                    pixies -= 1
            if xc < width-2:
                l = xc + 1
                if grid[y][l] != 1 and random.random() <= pixies/points:
                    grid[y][l] = 1
                    blacks.append((y,l))
                    used = True
                    new_blacks[0] = True
                    new_blacks[1] -= 1
                    pixies -= 1
    #
    for x in grid: print(x)


def grid1(width=24, height=30, pixies=0):
    points = width * height
    if pixies == 0:
        pixies = points // 3
    grid = [[0 for x in range(width)] for x in range(height)]
    x = random.randint(0, width-1)
    xc = x
    y = random.randint(0, height-1)
    #
    grid[y][x] = 1
    blacks = [(y,x)]
    new_blacks = [True, -1]
    pixies -= 1
    #
    # x may now be a list for some reason so beware...
    #
    use_these = []
    while pixies > 0:
        if new_blacks[0] == True:
            for a in range(-1, (new_blacks[1] - 1), -1):
                use_these.append(blacks[a])
            new_blacks = [False, 0]
            used = False
        for b in use_these:
            y = b[0]
            xc = b[1]
            if xc > 0:
                h = xc - 1
                if grid[y][h] != 1 and random.random() <= pixies/points:
                    grid[y][h] = 1
                    blacks.append((y,h))
                    used = True
                    new_blacks[0] = True
                    new_blacks[1] -= 1
                    pixies -= 1
            if y > 0:
                j = y - 1
                if grid[j][xc] != 1 and random.random() <= pixies/points:
                    grid[j][xc] = 1
                    blacks.append((j,xc))
                    used = True
                    new_blacks[0] = True
                    new_blacks[1] -= 1
                    pixies -= 1
            if y < height-2:
                k = y + 1
                if grid[k][xc] != 1 and random.random() <= pixies/points:
                    grid[k][xc] = 1
                    blacks.append((k,xc))
                    used = True
                    new_blacks[0] = True
                    new_blacks[1] -= 1
                    pixies -= 1
            if xc < width-2:
                l = xc + 1
                if grid[y][l] != 1 and random.random() <= pixies/points:
                    grid[y][l] = 1
                    blacks.append((y,l))
                    used = True
                    new_blacks[0] = True
                    new_blacks[1] -= 1
                    pixies -= 1
    #
    for x in grid: print(x)


def not_tiny(width=40, height=40, pixies=0):
    points = width * height
    if pixies == 0:
        pixies = points // 2
    grid = [[8 for x in range(width)] for x in range(height)]
    x = random.randint(0, width-1)
    xc = x
    y = random.randint(0, height-1)
    #
    grid[y][x] = 1
    blacks = [(y,x)]
    new_blacks = [True, -1]
    pixies -= 1
    #
    # x may now be a list for some reason so beware...
    #
    use_first = []
    #fib = 0
    while pixies > 0:
        if new_blacks[0] == True:
            for a in range(-1, (new_blacks[1] - 1), -1):
                use_first.append(blacks[a])
            new_blacks = [False, 0]
            used = False
        for b in use_first:
            y = b[0]
            xc = b[1]
            if xc > 0:
                h = xc - 1
                if grid[y][h] != 1 and random.random() <= pixies/points:
                    grid[y][h] = 1
                    blacks.append((y,h))
                    used = True
                    new_blacks[0] = True
                    use_first.remove(b)
                    new_blacks[1] -= 1
                    pixies -= 1
                    if pixies == 0:
                        break
            if y > 0:
                j = y - 1
                if grid[j][xc] != 1 and random.random() <= pixies/points:
                    grid[j][xc] = 1
                    blacks.append((j,xc))
                    used = True
                    new_blacks[0] = True
                    if b in use_first:
                        use_first.remove(b)
                    new_blacks[1] -= 1
                    pixies -= 1
                    if pixies == 0:
                        break
            if y < height-2:
                k = y + 1
                if grid[k][xc] != 1 and random.random() <= pixies/points:
                    grid[k][xc] = 1
                    blacks.append((k,xc))
                    used = True
                    new_blacks[0] = True
                    if b in use_first:
                        use_first.remove(b)
                    new_blacks[1] -= 1
                    pixies -= 1
                    if pixies == 0:
                        break
            if xc < width-2:
                l = xc + 1
                if grid[y][l] != 1 and random.random() <= pixies/points:
                    grid[y][l] = 1
                    blacks.append((y,l))
                    used = True
                    new_blacks[0] = True
                    if b in use_first:
                        use_first.remove(b)
                    new_blacks[1] -= 1
                    pixies -= 1
                    if pixies == 0:
                        break
        if used:
            continue
        else:
            blacks.reverse()
            for c in blacks:
                y = c[0]
                xc = c[1]
                if xc > 0:
                    h = xc - 1
                    if grid[y][h] != 1 and random.random() <= pixies/points:
                        grid[y][h] = 1
                        blacks.append((y,h))
                        new_blacks[0] = True
                        used = True
                        new_blacks[1] -= 1
                        pixies -= 1
                        if pixies == 0:
                            break
                if y > 0:
                    j = y - 1
                    if grid[j][xc] != 1 and random.random() <= pixies/points:
                        grid[j][xc] = 1
                        blacks.append((j,xc))
                        new_blacks[0] = True
                        used = True
                        new_blacks[1] -= 1
                        pixies -= 1
                        if pixies == 0:
                            break
                if y < height-2:
                    k = y + 1
                    if grid[k][xc] != 1 and random.random() <= pixies/points:
                        grid[k][xc] = 1
                        blacks.append((k,xc))
                        new_blacks[0] = True
                        used = True
                        new_blacks[1] -= 1
                        pixies -= 1
                        if pixies == 0:
                            break
                if xc < width-2:
                    l = xc + 1
                    if grid[y][l] != 1 and random.random() <= pixies/points:
                        grid[y][l] = 1
                        blacks.append((y,l))
                        new_blacks[0] = True
                        used = True
                        new_blacks[1] -= 1
                        pixies -= 1
                        if pixies == 0:
                            break
                if used:
                    blacks.reverse()
                    break
        if not used:
            blacks.reverse()
        #
        print('use_first:', use_first)
        print('new_blacks:', new_blacks)
        for x in grid: print(x)
    #
    print('Done!')
    for x in grid: print(x)


def double_grid(phrase, width=40, height=40, pixies=0):
    numbs = [ord(x) for x in phrase]
    #numbs = list(set(numbs))

    points = width * height
    if pixies == 0:
        pixies = points // 2
    grid = [[8 for x in range(width)] for x in range(height)]
    inverse = [[8 for x in range(width)] for x in range(height)]
    x = random.randint(0, width-1)
    xc = x
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
    fail_count = 0
    print(fail_count)
    #
    # x may now be a list for some reason so beware...
    #
    use_first = []
    four_loops = 0
    wild_loops = 0
    #
    while pixies > 0:
        wild_loops += 1
        if new_blacks[0] == True:
            for a in range(-1, (new_blacks[1] - 1), -1):
                use_first.append(blacks[a])
            new_blacks = [False, 0]
            used = False
        for b in use_first:
            four_loops += 1
            y = b[0]
            xc = b[1]
            if xc > 0:
                h = xc - 1
                if grid[y][h] != 1 and random.random() <= pixies/points and count != fib[0] and count % numbs[0] != 0:
                    grid[y][h] = 1
                    zy = height-1 - y
                    zx = width-1 - h
                    inverse[zy][zx] = 1
                    blacks.append((y,h))
                    used = True
                    new_blacks[0] = True
                    if b in use_first:
                        use_first.remove(b)
                    new_blacks[1] -= 1
                    pixies -= 1
                    count += 1
                    numbs = rotate(numbs)
                    if pixies == 0:
                        break
                if count == fib[0]:
                    fib.remove(count)         
            if y > 0:
                j = y - 1
                if grid[j][xc] != 1 and random.random() <= pixies/points and count != fib[0] and count % numbs[0] != 0:
                    grid[j][xc] = 1
                    zy = height-1 - j
                    zx = width-1 - xc
                    inverse[zy][zx] = 1
                    blacks.append((j,xc))
                    used = True
                    new_blacks[0] = True
                    if b in use_first:
                        use_first.remove(b)
                    new_blacks[1] -= 1
                    pixies -= 1
                    count += 1
                    numbs = rotate(numbs)
                    if pixies == 0:
                        break
                if count == fib[0]:
                    fib.remove(count)
            if y < height-2:
                k = y + 1
                if grid[k][xc] != 1 and random.random() <= pixies/points and count != fib[0] and count % numbs[0] != 0:
                    grid[k][xc] = 1
                    zy = height-1 - k
                    zx = width-1 - xc
                    inverse[zy][zx] = 1
                    blacks.append((k,xc))
                    used = True
                    new_blacks[0] = True
                    if b in use_first:
                        use_first.remove(b)
                    new_blacks[1] -= 1
                    pixies -= 1
                    count += 1
                    numbs = rotate(numbs)
                    if pixies == 0:
                        break
                if count == fib[0]:
                    fib.remove(count)
            if xc < width-2:
                l = xc + 1
                if grid[y][l] != 1 and random.random() <= pixies/points and count != fib[0] and count % numbs[0] != 0:
                    grid[y][l] = 1
                    zy = height-1 - y
                    zx = width-1 - l
                    inverse[zy][zx] = 1
                    blacks.append((y,l))
                    used = True
                    new_blacks[0] = True
                    if b in use_first:
                        use_first.remove(b)
                    new_blacks[1] -= 1
                    pixies -= 1
                    count += 1
                    numbs = rotate(numbs)
                    if pixies == 0:
                        break
                if count == fib[0]:
                    fib.remove(count)
        if used:
            fail_count = 0
            print(fail_count)
            continue
        else:
            fail_count += 1
            print(fail_count)
            #if fail_count > len(grid[0]) // 5:
            #    grid, inverse, blacks = whiten(grid, inverse, blacks, y, xc)
            #    fail_count = 0
            #    break
            blacks.reverse()
            for c in blacks:
                four_loops += 1
                y = c[0]
                xc = c[1]
                if xc > 0:
                    h = xc - 1
                    if grid[y][h] != 1 and random.random() <= pixies/points and count != fib[0] and count % numbs[0] != 0:
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
                        if pixies == 0:
                            break
                    if count == fib[0]:
                        fib.remove(count)
                    numbs = rotate(numbs)
                if y > 0:
                    j = y - 1
                    if grid[j][xc] != 1 and random.random() <= pixies/points and count != fib[0] and count % numbs[0] != 0:
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
                        if pixies == 0:
                            break
                    if count == fib[0]:
                        fib.remove(count)
                    numbs = rotate(numbs)
                if y < height-2:
                    k = y + 1
                    if grid[k][xc] != 1 and random.random() <= pixies/points and count != fib[0] and count % numbs[0] != 0:
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
                        if pixies == 0:
                            break
                    if count == fib[0]:
                        fib.remove(count)
                    numbs = rotate(numbs)
                if xc < width-2:
                    l = xc + 1
                    if grid[y][l] != 1 and random.random() <= pixies/points and count != fib[0] and count % numbs[0] != 0:
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
                        if pixies == 0:
                            break
                    if count == fib[0]:
                        fib.remove(count)
                    numbs = rotate(numbs)
                if used:
                    fail_count = 0
                    print(fail_count)
                    blacks.reverse()
                    break
        if not used:
            fail_count += 1
            print(fail_count)
            grid[y][xc] = 8
            zx = width-1 - xc
            zy = height-1 - y
            inverse[zy][zx] = 8
            pixies += 1
            blacks.reverse()
            #if fail_count > len(grid[0]) // 5:
            #    grid, inverse, blacks = whiten(grid, inverse, blacks)
            #    fail_count = 0
        #
        #print('use_first:', use_first)
        #print('new_blacks:', new_blacks)
        #for x in grid: print(x)
    #
    print('Done!')
    print('for loops:', four_loops)
    print('while loops:', wild_loops)
    print('Grid:')
    for x in grid: print(x)
    print('Inverse:')
    for x in inverse: print(x)


def whiten(grid, inverse, blacks, y, xc):
    pass