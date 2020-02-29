# Remember, if you make things TOO random, it will all just come out gray looking.

# based upon their relative frequency in the english language:
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


base_A = random.random()
upper_A = (base_A + 0.25) if ((base_A + 0.25) <= 1) else (base_A - 0.75)
lower_A = (base_A - 0.25) if ((base_A - 0.25) >= 0) else (base_A + 0.75)
base_B = flip(base_A)
upper_B = (base_B + 0.25) if ((base_B + 0.25) <= 1) else (base_B - 0.75)
lower_B = (base_B - 0.25) if ((base_B - 0.25) >= 0) else (base_B + 0.75)


# these should be constants
import random
from PIL import Image
hue = random.random()
lightness = 0.5
saturation = 1
hls = [hue, lightness, saturation]
def mode_conversion(hls):
    # convert from hue-lightness-saturation to rgb for PIL:
    # hls_toopull must have three values between 0 and 1, not 1 and 360
    import colorsys
    rgb = [(255 * x) for x in colorsys.hls_to_rgb(*hls)]
    image = Image.new('RGB', (40, 40), color=(rgb[0], rgb[1], rgb[2]))
    image.show()


def shift_prob(key):
    shift_denom = relatives['e']
    return (relatives[key] / shift_denom)


def switch_prob(key):
    switch_numerator = relatives['z']
    return (switch_numerator / relatives[key])


def switch(direction, key):
    if random.random() < switch_prob(key):
        if self.direction == True:
            self.direction = False
        else:
            self.direction = True


def shift(rising, upper, lower, key, val):
    impressions += 1
    if random.random() < shift_prob(key):
        if rising:
            if (val + 0.01) <= upper:
                if (val + 0.01) <= 1:
                    return val + 0.01
                else:
                    return val - 0.99
            else:
                self.rising = False
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
                self.rising = True
                if (val + 0.01) <= 1:
                    return val + 0.01
                else:
                    return val - 0.99


def flip(x):
    x += 0.5
    if x > 1:
        x -= 1
    return x