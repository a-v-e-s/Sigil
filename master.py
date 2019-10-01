"""
make_sigil.py: Turn a statement into a symbol only the subconscious 
mind can possibly decode. Must be run from the directory of the script
or else font_options list comprehension won't work.
Under active development.

Author: Jon David Tannehill
"""

from PIL import Image, ImageFont, ImageDraw, ImageOps
import tkinter as tk
from tkinter.filedialog import askdirectory
import os, sys, random, math, factors


class Gui():
    def __init__(self):
        # initialize the widgets, variables, etc.
        self.root = tk.Tk()
        self.root.title('Sigil Maker')
        tk.Label(self.root, text='Enter the text you wish to turn into'
            'a sigil:').grid(row=1, column=1, columnspan=2)
        self.rownum = 9
        self.phrases = []
        self.entries = []
        self.chop_width = tk.IntVar()
        self.chop_height = tk.IntVar()
        # These may later be turned into regular ints, but for now I'm
        # keeping them as tkinter IntVars
        # in case I decide to allow the user to adjust them again as I
        # did in the previous version.
        self.chop_width.set(10)
        self.chop_height.set(10)
        self.colorized = tk.IntVar()
        self.show = tk.IntVar()
        self.dir = tk.StringVar()
        a = tk.Button(self.root)
        b = tk.Button(self.root)
        c = tk.Label(self.root)
        d = tk.Checkbutton(self.root)
        e = tk.Label(self.root)
        f = tk.Checkbutton(self.root)
        g = tk.Label(self.root)
        h = tk.Entry(self.root)
        i = tk.Button(self.root)
        z = tk.Button(self.root)
        self.widgets = [a, b, c, d, e, f, g, h, i, z]
        a.configure(text='Add Another', command=self.add_entry)
        a.grid(row=self.rownum-5, column=1)
        b.configure(text='Delete Previous', command=self.remove)
        b.grid(row=self.rownum-5, column=2)
        c.configure(text='Colorize:')
        c.grid(row=self.rownum-4, column=1)
        d.configure(variable=self.colorized, offvalue=0, onvalue=1)
        d.grid(row=self.rownum-4, column=2)
        e.configure(text='Automatically show resulting image?')
        e.grid(row=self.rownum-3, column=1)
        f.configure(variable=self.show, offvalue=0, onvalue=1)
        f.grid(row=self.rownum-3, column=2)
        g.configure(text='\nChoose folder to save images in or default'
            'to\n' + os.getcwd() + ':')
        g.grid(row=self.rownum-2, column=1)
        h.configure(textvariable=self.dir, width=40)
        h.grid(row=self.rownum-1, column=1)
        i.configure(text='Browse', command=(lambda x=h:[x.delete(0,
            len(x.get())), x.insert(0, askdirectory())]))
        i.grid(row=self.rownum-1, column=2)
        z.configure(text='Go!', command=self.make_sigil)
        z.grid(row=self.rownum, column=1, columnspan=2)

        # add room for two statements, and set the options to defaults
        self.add_entry()
        self.add_entry()
        d.deselect()
        f.deselect()
        self.entries[0].focus_set()
        
        # keybindings
        self.root.bind(sequence='<Return>', func=(lambda
            x=self.make_sigil: self.make_sigil()))
        self.root.bind(sequence='<Control-KeyPress-n>', func=(lambda
            y=self.add_entry: self.add_entry()))
        self.root.bind(sequence='<Control-KeyPress-d>', func=(lambda
            z=self.remove: self.remove()))


    def add_entry(self):
        # create new entry widget and variable for it
        text = tk.StringVar()
        entry = tk.Entry(self.root, width=60, textvariable=text)
        entry.grid(row=self.rownum-6, column=1, columnspan=2)
        self.phrases.append(text)
        self.entries.append(entry)
        
        # adjust other widgets accordingly
        self.rownum += 1
        self.reposition()

    
    def remove(self):
        # remove the entry widget and its variable
        del self.phrases[-1]
        self.entries[-1].grid_forget()
        del self.entries[-1]

        # adjust widgets accordingly
        self.rownum -= 1
        self.reposition()

    
    def reposition(self):
        self.widgets[0].grid(row=self.rownum-5, column=1)
        self.widgets[1].grid(row=self.rownum-5, column=2)
        self.widgets[2].grid(row=self.rownum-4, column=1)
        self.widgets[3].grid(row=self.rownum-4, column=2)
        self.widgets[4].grid(row=self.rownum-3, column=1)
        self.widgets[5].grid(row=self.rownum-3, column=2)
        self.widgets[6].grid(row=self.rownum-2, column=1)
        self.widgets[7].grid(row=self.rownum-1, column=1)
        self.widgets[8].grid(row=self.rownum-1, column=2)
        self.widgets[9].grid(row=self.rownum, column=1, columnspan=2)
        

    def make_sigil(self):
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

            # save and display the sigil:
            sigil.save(os.path.join(self.dir.get(),
                ''.join([str(ord(x)) for x in text[-4:]]) + '.png'),
                'PNG')
            if self.show.get() == 1:
                sigil.show()
            

if __name__ == '__main__':
    gui = Gui()
    gui.root.mainloop()