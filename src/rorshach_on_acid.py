#!/usr/bin/trip_the_F_out

import random, pickle, fibonacci, colorsys

fib = fibonacci.make_fibonacci(1000)[4:]
hue_shift = random.random()
lightness = 0.5
saturation = 1
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


class Rorshach():
    def __init__(self, phrase, width=100, height=100):
        self.original_phrase, self.phrase, self.width, self.height = phrase, phrase, width, height
        self.base_A = 0.25
        self.upper_A = 0.5
        self.lower_A = 0
        self.base_B = 0.75
        self.upper_B = 1
        self.lower_B = 0.5
        self.codename = hex(hash(phrase))[2:]
        self.numbs = [ord(x) for x in phrase]
        self.grid = [[self.base_A for x in range(width)] for x in range(height)]
        self.points = width * height
        self.pixies = self.points // 2
        self.impressions = 0
        #


    def switch_prob(self, key):
        try:
            # experiment with different values for the constant here:
            return ((switch_numerator / relatives[key]) * 0.08)
        except KeyError:
            return 0


    def switch(self, rising, key):
        if random.random() < self.switch_prob(key):
            if rising == True:
                rising = False
            else:
                rising = True
        return rising


    def shift_prob(self, key):
        # this is probably returning values that are too high on average,
        # causing shift to shift too little...
        try:
            return (relatives[key] / shift_denominator)
        except KeyError:
            return 0


    def shift(self, rising, upper, lower, key, val):
        print(type(val))
        self.impressions += 1
        if random.random() < self.shift_prob(key):
            if rising:
                if (val + 0.01) <= upper:
                    if (val + 0.01) <= 1:
                        return val + 0.01
                    else:
                        return val - 0.99
                else:
                    rising = False
                    if (val - 0.01) >= 0:
                        return val - 0.01
                    else:
                        return val + 0.99
            else:
                if (val - 0.01) >= lower:
                    if (val - 0.01) >= 0:
                        return val - 0.01
                    else:
                        return val + 0.99
                else:
                    rising = True
                    if (val + 0.01) <= 1:
                        return val + 0.01
                    else:
                        return val - 0.99
        else:
            return val
    

    def darken(self):
        rising = random.choice([True, False])
        # set initial coordinates at random:
        x = random.randint(0, self.width-1)
        xc = x    # I don't understand why this is necessary but it is.
        y = random.randint(0, self.height-1)
        #
        self.grid[y][x] = random.uniform(0.5, 1)
        Bs = [(y,x)]
        new_Bs = [True, -1]
        self.pixies -= 1
        count = 1
        use_first = []
        fail_count = 0
        whitened = False
        #
        # begin the loop!
        while self.pixies > 0:
            #try:
            #    progress[codename] = impressions
            #except Exception:
            #    pass
            if whitened:
                x = random.randint(0, self.width-1)
                y = random.randint(0, self.height-1)
                xc = x
                if self.upper_A >= self.grid[y][x] >= self.lower_A:
                    # make this more random:
                    self.grid[y][x] = random.uniform(0.5, 1)
                    self.pixies -= 1
                    count += 1
                    Bs.append((y,xc))
                    use_first.append((y,xc))
                    new_Bs = [True, -1]
                    whitened = False
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
                    if self.grid[y][h] < 0.5 and random.random() <= self.pixies/self.points and count != fib[0]:
                        self.impressions += 1
                        if count % self.numbs[0] != 0:
                            print(self.grid[b[0]][b[1]])
                            self.grid[y][h] = self.shift(rising, self.upper_B, self.lower_B, self.phrase[0], self.grid[b[0]][b[1]])
                            rising = self.switch(rising, self.phrase[0])
                            count += 1
                            self.pixies -= 1
                            used = True
                            Bs.append((y,h))
                            new_Bs[0] = True
                            new_Bs[1] -= 1
                            use_first.remove(b)
                            if self.pixies == 0:
                                break      
                        self.numbs = self.numbs[1:] + self.numbs[:1]
                        self.phrase = self.phrase[1:] + self.phrase[:1]
                    if count == fib[0]:
                        fib.remove(count)
                if y > 0:
                    j = y - 1
                    if self.grid[j][xc] < 0.5 and random.random() <= self.pixies/self.points and count != fib[0]:
                        self.impressions += 1
                        if count % self.numbs[0] != 0:
                            print(self.grid[b[0]][b[1]])
                            self.grid[j][xc] = self.shift(rising, self.upper_B, self.lower_B, self.phrase[0], self.grid[b[0]][b[1]])
                            rising = self.switch(rising, self.phrase[0])
                            count += 1
                            self.pixies -= 1
                            used = True
                            Bs.append((j,xc))
                            new_Bs[0] = True
                            new_Bs[1] -= 1
                            if b in use_first:
                                use_first.remove(b)
                            if self.pixies == 0:
                                break
                        self.numbs = self.numbs[1:] + self.numbs[:1]
                        self.phrase = self.phrase[1:] + self.phrase[:1]
                    if count == fib[0]:
                        fib.remove(count)
                if y < self.height-2:
                    k = y + 1
                    if self.grid[k][xc] < 0.5 and random.random() <= self.pixies/self.points and count != fib[0]:
                        self.impressions += 1
                        if count % self.numbs[0] != 0:
                            print(self.grid[b[0]][b[1]])
                            self.grid[k][xc] = self.shift(rising, self.upper_B, self.lower_B, self.phrase[0], self.grid[b[0]][b[1]])
                            rising = self.switch(rising, self.phrase[0])
                            count += 1
                            self.pixies -= 1
                            used = True
                            Bs.append((k,xc))
                            new_Bs[0] = True
                            new_Bs[1] -= 1
                            if b in use_first:
                                use_first.remove(b)
                            if self.pixies == 0:
                                break
                        self.numbs = self.numbs[1:] + self.numbs[:1]
                        self.phrase = self.phrase[1:] + self.phrase[:1]
                    if count == fib[0]:
                        fib.remove(count)
                if xc < self.width-2:
                    l = xc + 1
                    if self.grid[y][l] < 0.5 and random.random() <= self.pixies/self.points and count != fib[0]:
                        self.impressions += 1
                        if count % self.numbs[0] != 0:
                            print(self.grid[b[0]][b[1]])
                            self.grid[y][l] = self.shift(rising, self.upper_B, self.lower_B, self.phrase[0], self.grid[b[0]][b[1]])
                            rising = self.switch(rising, self.phrase[0])
                            count += 1
                            self.pixies -= 1
                            used = True
                            Bs.append((y,l))
                            new_Bs[0] = True
                            new_Bs[1] -= 1
                            if b in use_first:
                                use_first.remove(b)
                            if self.pixies == 0:
                                break
                        self.numbs = self.numbs[1:] + self.numbs[:1]
                        self.phrase = self.phrase[1:] + self.phrase[:1]
                    if count == fib[0]:
                        fib.remove(count)
            if used:
                fail_count = 0
                continue
            else:
                fail_count += 1
                if fail_count > len(self.grid[0]) // 24:
                    Bs = self.whiten(
                        Bs
                    )
                    use_first = []
                    fail_count = 0
                    whitened = True
                    continue
                Bs.reverse()
                for c in Bs:
                    y = c[0]
                    xc = c[1]
                    if xc > 0:
                        h = xc - 1
                        if self.grid[y][h] < 0.5 and random.random() <= self.pixies/self.points and count != fib[0]:
                            self.impressions += 1
                            if count % self.numbs[0] != 0:
                                print(self.grid[b[0]][b[1]])
                                self.grid[y][h] = self.shift(rising, self.upper_B, self.lower_B, self.phrase[0], self.grid[c[0]][c[1]])
                                rising = self.switch(rising, self.phrase[0])
                                count += 1
                                self.pixies -= 1
                                used = True
                                Bs.append((y,h))
                                new_Bs[0] = True
                                new_Bs[1] -= 1
                                self.numbs = self.numbs[1:] + self.numbs[:1]
                                self.phrase = self.phrase[1:] + self.phrase[:1]
                                if self.pixies == 0:
                                    break
                        if count == fib[0]:
                            fib.remove(count)
                    if y > 0:
                        j = y - 1
                        if self.grid[j][xc] < 0.5 and random.random() <= self.pixies/self.points and count != fib[0]:
                            self.impressions += 1
                            if count % self.numbs[0] != 0:
                                print(self.grid[b[0]][b[1]])
                                self.grid[j][xc] = self.shift(rising, self.upper_B, self.lower_B, self.phrase[0], self.grid[c[0]][c[1]])
                                rising = self.switch(rising, self.phrase[0])
                                count += 1
                                self.pixies -= 1
                                used = True
                                Bs.append((j,xc))
                                new_Bs[0] = True
                                new_Bs[1] -= 1
                                self.numbs = self.numbs[1:] + self.numbs[:1]
                                self.phrase = self.phrase[1:] + self.phrase[:1]
                                if self.pixies == 0:
                                    break
                        if count == fib[0]:
                            fib.remove(count)
                    if y < self.height-2:
                        k = y + 1
                        if self.grid[k][xc] < 0.5 and random.random() <= self.pixies/self.points and count != fib[0]:
                            self.impressions += 1
                            if count % self.numbs[0] != 0:
                                print(self.grid[b[0]][b[1]])
                                self.grid[k][xc] = self.shift(rising, self.upper_B, self.lower_B, self.phrase[0], self.grid[c[0]][c[1]])
                                rising = self.switch(rising, self.phrase[0])
                                count += 1
                                self.pixies -= 1
                                used = True
                                Bs.append((k,xc))
                                new_Bs[0] = True
                                new_Bs[1] -= 1
                                self.numbs = self.numbs[1:] + self.numbs[:1]
                                self.phrase = self.phrase[1:] + self.phrase[:1]
                                if self.pixies == 0:
                                    break
                        if count == fib[0]:
                            fib.remove(count)
                    if xc < self.width-2:
                        l = xc + 1
                        if self.grid[y][l] < 0.5 and random.random() <= self.pixies/self.points and count != fib[0]:
                            self.impressions += 1
                            if count % self.numbs[0] != 0:
                                print(self.grid[b[0]][b[1]])
                                self.grid[y][l] = self.shift(rising, self.upper_B, self.lower_B, self.phrase[0], self.grid[c[0]][c[1]])
                                rising = self.switch(rising, self.phrase[0])
                                count += 1
                                self.pixies -= 1
                                used = True
                                Bs.append((y,l))
                                new_Bs[0] = True
                                new_Bs[1] -= 1
                                self.numbs = self.numbs[1:] + self.numbs[:1]
                                self.phrase = self.phrase[1:] + self.phrase[:1]
                                if self.pixies == 0:
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
                    if fail_count > len(self.grid[0]) // 24:
                        Bs = self.whiten(Bs)
                        use_first = []
                        fail_count = 0
                        whitened = True
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
        for row in self.grid:
            rownum += 1
            colnum = -1
            for x in row:
                colnum += 1
                self.grid[rownum][colnum] = [round((255 * c)) for c in colorsys.hls_to_rgb(x, lightness, saturation)]

        # return if testing:
        if self.original_phrase == 'turtle clucker.':
            return self.grid#, inverse
        """
        # save to grids pickle file if not testing:
        # final impression count:
        try:
            #progress[codename] = impressions
        except Exception:
            pass
        #
        save_this = (inverse, phrase)
        try:
            with open('grids.pkl', 'rb') as f:
                grids = pickle.load(f)
            grids.append(save_this)
            with open('grids.pkl', 'wb') as f:
                pickle.dump(grids, f)
        except EOFError:
            grids = []
            grids.append(save_this)
            with open('grids.pkl', 'wb') as f:
                pickle.dump(grids, f)
        except FileNotFoundError:
            grids = []
            grids.append(save_this)
            with open('grids.pkl', 'wb') as f:
                pickle.dump(grids, f)
        """


    def whiten(self, Bs):
        rising = random.choice([True, False])
        #r = random.choice(Bs)
        y = random.choice(range(self.height))
        xc = random.choice(range(self.width))
        self.grid[y][xc] = random.uniform(0, 0.5)
        As = [(y,xc)]
        new_As = [True, -1]
        self.pixies += 1
        use_first = []
        whitening = True
        while whitening:
            #try:
            #    progress[codename] = impressions
            #except Exception:
            #    pass
            whitening = False
            for a in range(-1, (new_As[1] - 1), -1):
                use_first.append(As[a])
            new_As = [False, 0]
            for w in use_first:
                whitened = 1
                y = w[0]
                xc = w[1]
                if xc > 0:
                    h = xc - 1
                    if self.grid[y][h] > 0.5 and random.random() >= len(As)/len(Bs) and whitened != fib[0]:
                        self.impressions += 1
                        if self.numbs[0] % whitened == 0:
                            print(self.grid[w[0]][w[1]])
                            self.grid[y][h] = self.shift(rising, self.upper_A, self.lower_A, self.phrase[0], self.grid[w[0]][w[1]])
                            rising = self.switch(rising, self.phrase[0])
                            whitening = True
                            whitened += 1
                            self.pixies += 1
                            As.append((y,h))
                            new_As[0] = True
                            new_As[1] -= 1
                            Bs.remove((y,h))
                            use_first.remove(w)
                        self.numbs = self.numbs[1:] + self.numbs[:1]
                        self.phrase = self.phrase[1:] + self.phrase[:1]
                    if whitened == fib[0]:
                        fib.remove(whitened)
                if y > 0:
                    j = y - 1
                    if self.grid[j][xc] > 0.5 and random.random() >= len(As)/len(Bs) and whitened != fib[0]:
                        self.impressions += 1
                        if self.numbs[0] % whitened == 0:
                            print(self.grid[w[0]][w[1]])
                            self.grid[j][xc] = self.shift(rising, self.upper_A, self.lower_A, self.phrase[0], self.grid[w[0]][w[1]])
                            rising = self.switch(rising, self.phrase[0])
                            whitening = True
                            whitened += 1
                            self.pixies += 1
                            As.append((j,xc))
                            new_As[0] = True
                            new_As[1] -= 1
                            Bs.remove((j,xc))
                            if w in use_first:
                                use_first.remove(w)
                        self.numbs = self.numbs[1:] + self.numbs[:1]
                        self.phrase = self.phrase[1:] + self.phrase[:1]
                    if whitened == fib[0]:
                        fib.remove(whitened)
                if y < self.height-2:
                    k = y + 1
                    if self.grid[k][xc] > 0.5 and random.random() >= len(As)/len(Bs) and whitened != fib[0]:
                        self.impressions += 1
                        if self.numbs[0] % whitened == 0:
                            print(self.grid[w[0]][w[1]])
                            self.grid[k][xc] = self.shift(rising, self.upper_A, self.lower_A, self.phrase[0], self.grid[w[0]][w[1]])
                            rising = self.switch(rising, self.phrase[0])
                            whitening = True
                            whitened += 1
                            self.pixies += 1
                            As.append((k,xc))
                            new_As[0] = True
                            new_As[1] -= 1
                            Bs.remove((k,xc))
                            if w in use_first:
                                use_first.remove(w)
                        self.numbs = self.numbs[1:] + self.numbs[:1]
                        self.phrase = self.phrase[1:] + self.phrase[:1]
                    if whitened == fib[0]:
                        fib.remove(whitened)
                if xc < self.width-2:
                    l = xc + 1
                    if self.grid[y][l] > 0.5 and random.random() >= len(As)/len(Bs) and whitened != fib[0]:
                        self.impressions += 1
                        if self.numbs[0] % whitened == 0:
                            print(self.grid[w[0]][w[1]])
                            self.grid[y][l] = self.shift(rising, self.upper_A, self.lower_A, self.phrase[0], self.grid[w[0]][w[1]])
                            rising = self.switch(rising, self.phrase[0])
                            whitening = True
                            whitened += 1
                            self.pixies += 1
                            As.append((y,l))
                            new_As[0] = True
                            new_As[1] -= 1
                            Bs.remove((y,l))
                            if w in use_first:
                                use_first.remove(w)
                        self.numbs = self.numbs[1:] + self.numbs[:1]
                        self.phrase = self.phrase[1:] + self.phrase[:1]
                    if whitened == fib[0]:
                        fib.remove(whitened)
        #
        return Bs


if __name__ == '__main__':
    # testing code:
    from PIL import Image
    phrase = 'turtle clucker.'
    a = Rorshach(phrase)
    # this takes a stupendously long time to run, even when the grid is TINY
    # why is that???
    grid = a.darken()
    print('impressions:', a.impressions)
    #
    image = Image.new('RGB', (100, 100), color=(0, 0, 0))
    pic1 = image.load()
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            pic1[x,y] = tuple(grid[y][x])
    image.show()