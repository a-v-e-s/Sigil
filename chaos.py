import os, math, random
from PIL import Image, ImageFont, ImageDraw, ImageOps

def scramble():
    
    font_options = []
    for x in os.listdir('fonts'):
        font_options.append(os.path.join(os.getcwd(), 'fonts', x))

    for a in self.phrases:
        # make an image out of the text in each entry
        # make its size a multiple of the chop_sizes
        font = ImageFont.truetype(font=random.choice(font_options),
            size=48, encoding='unic')
        text = a.get()
        text_width, text_height = font.getsize(text)
        if text_width % self.chop_width.get() != 0:
            text_width += (self.chop_width.get() -
                (text_width % self.chop_width.get()))
        if text_height % self.chop_height.get() != 0:
            text_height += (self.chop_height.get() -
                (text_height % self.chop_height.get()))
        canvas = Image.new('L', (text_width, text_height), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((0, 0), text, 'black', font)

        # if user wanted it colorized, colorize it randomly
        if self.colorized.get():
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
        for w in range(0, img_width, self.chop_width.get()):
            for h in range(0, img_height, self.chop_height.get()):
                # are the elif, else conditions still necessary now
                # that original canvas size is modified?
                if ((w + self.chop_width.get() < img_width) and
                    (h + self.chop_height.get() < img_height)):
                    box = (w, h, w+self.chop_width.get(),
                        h+self.chop_height.get())
                elif ((w + self.chop_width.get() < img_width) and
                    (h + self.chop_height.get() >= img_height)):
                    box = (w, h, w+self.chop_width.get(),
                        img_height)
                elif ((w + self.chop_width.get() >= img_width) and
                    (h + self.chop_height.get() < img_height)):
                    box = (w, h, img_width,
                        h+self.chop_height.get())
                else:
                    box = (w, h, img_width, img_height)
                blocks.append(canvas.crop(box))
        
        # prepare the new image
        if (factors.factor_combinations(len(blocks))[-1][1] >
            (3 * factors.factor_combinations(len(blocks))[-1][0])):
            sigil_width = (math.ceil(math.sqrt(len(blocks))) *
                self.chop_width.get())
            sigil_height = (math.ceil(math.sqrt(len(blocks))) *
                self.chop_height.get())
            blanks = ((math.ceil(math.sqrt(len(blocks))) ** 2) -
                len(blocks) + 1)
            for x in range(1, blanks):
                if self.colorized.get():
                   blocks.append(Image.new('RGB',
                        (self.chop_width.get(),
                        self.chop_height.get()),
                        color=background_color))
                else:
                    blocks.append(Image.new('RGB',
                        (self.chop_width.get(),
                        self.chop_height.get()),
                        color=(255,255,255)))
        else:
            sigil_width = factors.factor_combinations(
                len(blocks))[-1][0] * self.chop_width.get()
            sigil_height = factors.factor_combinations(
                len(blocks))[-1][1] * self.chop_height.get()
        x, y = 0, 0
        position = (x, y)
        sigil = Image.new('RGB', (sigil_width, sigil_height),
            'white')

        # shuffle and put the pieces into place
        random.shuffle(blocks)
        for b in blocks:
            sigil.paste(b, box=position)
            if (position[0] + self.chop_width.get()) < sigil_width:
                x += self.chop_width.get()
            else:
                x = 0
                y += self.chop_height.get()
            position = (x, y)
