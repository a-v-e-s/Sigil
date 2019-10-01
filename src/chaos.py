import os, math, random, factors
from PIL import Image, ImageFont, ImageDraw, ImageOps


def scramble(phrases, colorized=1, chop_width=10, chop_height=10):
    font_options = []
    for x in os.listdir('fonts'):
        font_options.append(os.path.join(os.getcwd(), 'fonts', x))

    random.shuffle(phrases)
    for phrase in phrases:
        # make an image out of the text in each entry
        # make its size a multiple of the chop_sizes
        font = ImageFont.truetype(font=random.choice(font_options),
            size=48, encoding='unic')
        text_width, text_height = font.getsize(phrase)
        if text_width % chop_width != 0:
            text_width += (chop_width -
                (text_width % chop_width))
        if text_height % chop_height != 0:
            text_height += (chop_height -
                (text_height % chop_height))
        canvas = Image.new('L', (text_width, text_height), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((0, 0), phrase, 'black', font)

        # if user wanted it colorized, colorize it randomly
        if colorized:
            text_color = (random.choice(range(255)),
                random.choice(range(255)),
                random.choice(range(255)))
            background_color = (random.choice(range(255)),
                random.choice(range(255)),
                random.choice(range(255)))
            mid = (random.choice(range(255)),
                random.choice(range(255)),
                random.choice(range(255)))
            midpoint = random.choice(range(84, 170))
            blackpoint = random.choice(range(0, 42))
            whitepoint = random.choice(range(212, 255))
            canvas = ImageOps.colorize(canvas, text_color,
                background_color, mid, blackpoint, whitepoint, midpoint)

        # chop the image of the text up into bite-sized blocks
        img_width, img_height = canvas.size
        blocks = []
        for w in range(0, img_width, chop_width):
            for h in range(0, img_height, chop_height):
                # are the elif, else conditions still necessary now
                # that original canvas size is modified?
                if ((w + chop_width < img_width) and
                    (h + chop_height < img_height)):
                    box = (w, h, w+chop_width,
                        h+chop_height)
                elif ((w + chop_width < img_width) and
                    (h + chop_height >= img_height)):
                    box = (w, h, w+chop_width,
                        img_height)
                elif ((w + chop_width >= img_width) and
                    (h + chop_height < img_height)):
                    box = (w, h, img_width,
                        h+chop_height)
                else:
                    box = (w, h, img_width, img_height)
                blocks.append(canvas.crop(box))
        
        # prepare the new image
        if (factors.factor_combinations(len(blocks))[-1][1] >
            (3 * factors.factor_combinations(len(blocks))[-1][0])):
            img_width = (math.ceil(math.sqrt(len(blocks))) *
                chop_width)
            img_height = (math.ceil(math.sqrt(len(blocks))) *
                chop_height)
            blanks = ((math.ceil(math.sqrt(len(blocks))) ** 2) -
                len(blocks) + 1)
            for x in range(1, blanks):
                if colorized:
                   blocks.append(Image.new('RGB',
                        (chop_width,
                        chop_height),
                        color=background_color))
                else:
                    blocks.append(Image.new('RGB',
                        (chop_width,
                        chop_height),
                        color=(255,255,255)))
        else:
            img_width = factors.factor_combinations(
                len(blocks))[-1][0] * chop_width
            img_height = factors.factor_combinations(
                len(blocks))[-1][1] * chop_height
        x, y = 0, 0
        position = (x, y)
        img = Image.new('RGB', (img_width, img_height),
            'white')

        # shuffle and put the pieces into place
        random.shuffle(blocks)
        for b in blocks:
            img.paste(b, box=position)
            if (position[0] + chop_width) < img_width:
                x += chop_width
            else:
                x = 0
                y += chop_height
            position = (x, y)

        yield [img, phrase]
