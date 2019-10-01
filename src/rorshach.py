import random, os, math
from factors import factor_combinations
from PIL import Image, ImageFont, ImageDraw, ImageOps


def inkblot(phrases, colorized):
    font_options = []
    for x in os.listdir('fonts'):
        font_options.append(os.path.join(os.getcwd(), 'fonts', x))

    random.shuffle(phrases)
    for phrase in phrases:
        font = ImageFont.truetype(font=random.choice(font_options), size=48, encoding='unic')
    	text_width, text_height = font.getsize(phrase)
    	canvas = Image.new('L', (text_width, text_height), "white")
    	draw = ImageDraw.Draw(canvas)
    	draw.text((0, 0), phrase, 'black', font)
    	pixels = list(canvas.getdata())

        pixies = 0
        for x in pixels:
            if x != 255:
                pixies += 1
        
        if factor_combinations(len(pixels))[-1][1] > (3 * factor_combinations(len(pixels))[-1][0]):
            width = math.ceil(math.sqrt(len(pixels)))
            height = math.ceil(math.sqrt(len(pixels)))
        else:
            width = factor_combinations(len(pixels))[-1][0]
            height = factor_combinations(len(pixels))[-1][1]

        if colorized:
            background = (random.choice(range(255)), random.choice(range(255)), random.choice(range(255)))
            img = Image.new(RGB, (width, height), color=background)
        else:
            img = Image.new(L, (width, height), color=(255,255,255))

        