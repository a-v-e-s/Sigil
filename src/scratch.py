# Remember, if you make things TOO random, it will all just come out gray looking.

def invert(color):
    new_values = []
    new_values.append(255-color[0])
    new_values.append(255-color[1])
    new_values.append(255-color[2])
    return new_values

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

def shift(color, character, channel):
    if channel = 'R':
        pass
    elif channel = 'G':
        pass
    elif channel = 'B':
        pass
    else:
        invert(color)