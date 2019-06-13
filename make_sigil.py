"""
make_sigil.py: Turn a statement into a symbol only the subconscious mind can possibly decode.

Under active development.

Author: Jon David Tannehill
"""

from PIL import Image, ImageFont, ImageDraw, ImageOps
import tkinter as tk
import subprocess, sys, random, math, factors


class Gui():
    def __init__(self):
        # initialize the widgets, variables, etc.
        self.root = tk.Tk()
        self.root.title('Sigil Maker')
        tk.Label(self.root, text='Enter the text you wish to turn into a sigil:').grid(row=1, column=1, columnspan=2)
        self.rownum = 8
        self.phrases = []
        self.entries = []
        self.chop_width = tk.IntVar()
        self.chop_height = tk.IntVar()
        self.colorized = tk.IntVar()
        a = tk.Button(self.root)
        b = tk.Button(self.root)
        c = tk.Label(self.root)
        d = tk.Scale(self.root)
        e = tk.Label(self.root)        
        f = tk.Scale(self.root)
        g = tk.Label(self.root)
        h = tk.Checkbutton(self.root)
        z = tk.Button(self.root)
        self.widgets = [a, b, c, d, e, f, g, h, z]
        a.configure(text='Add Another', command=self.add_entry)
        a.grid(row=self.rownum-4, column=1)
        b.configure(text='Delete Previous', command=self.remove)
        b.grid(row=self.rownum-4, column=2)
        c.configure(text='Chop width:')
        c.grid(row=self.rownum-3, column=1)
        d.configure(from_=8, to=16, variable=self.chop_width, orient='horizontal')
        d.grid(row=self.rownum-3, column=2)
        e.configure(text='Chop height:')
        e.grid(row=self.rownum-2, column=1)
        f.configure(from_=8, to=16, variable=self.chop_height, orient='horizontal')
        f.grid(row=self.rownum-2, column=2)
        g.configure(text='Colorize:')
        g.grid(row=self.rownum-1, column=1)
        h.configure(variable=self.colorized, offvalue=0, onvalue=1)
        h.grid(row=self.rownum-1, column=2)
        z.configure(text='Go!', command=self.make_sigil)
        z.grid(row=self.rownum, column=1, columnspan=2)

        # add room for two statements, and set the options to their defaults
        self.add_entry()
        self.add_entry()
        self.chop_width.set(10)
        self.chop_height.set(10)
        h.deselect()
        self.entries[0].focus_set()
        
        # keybindings
        self.root.bind(sequence='<Return>', func=(lambda x=self.make_sigil: self.make_sigil()))
        self.root.bind(sequence='<Control-KeyPress-n>', func=(lambda y=self.add_entry: self.add_entry()))
        self.root.bind(sequence='<Control-KeyPress-d>', func=(lambda z=self.remove: self.remove()))


    def add_entry(self):
        # create new entry widget and variable for it
        text = tk.StringVar()
        entry = tk.Entry(self.root, width=40, textvariable=text)
        entry.grid(row=self.rownum-6, column=1, columnspan=2)
        self.phrases.append(text)
        self.entries.append(entry)
        
        # adjust other widgets accordingly
        self.rownum += 1
        self.widgets[0].grid(row=self.rownum-4, column=1)
        self.widgets[1].grid(row=self.rownum-4, column=2)
        self.widgets[2].grid(row=self.rownum-3, column=1)
        self.widgets[3].grid(row=self.rownum-3, column=2)
        self.widgets[4].grid(row=self.rownum-2, column=1)
        self.widgets[5].grid(row=self.rownum-2, column=2)
        self.widgets[6].grid(row=self.rownum-1, column=1)
        self.widgets[7].grid(row=self.rownum-1, column=2)
        self.widgets[8].grid(row=self.rownum, column=1, columnspan=2)

    
    def remove(self):
        # remove the entry widget and its variable
        del self.phrases[-1]
        self.entries[-1].grid_forget()
        del self.entries[-1]

        # adjust widgets accordingly
        self.rownum -= 1
        self.widgets[0].grid(row=self.rownum-4, column=1)
        self.widgets[1].grid(row=self.rownum-4, column=2)
        self.widgets[2].grid(row=self.rownum-3, column=1)
        self.widgets[3].grid(row=self.rownum-3, column=2)
        self.widgets[4].grid(row=self.rownum-2, column=1)
        self.widgets[5].grid(row=self.rownum-2, column=2)
        self.widgets[6].grid(row=self.rownum-1, column=1)
        self.widgets[7].grid(row=self.rownum-1, column=2)
        self.widgets[8].grid(row=self.rownum, column=1, columnspan=2)
        

    def make_sigil(self):
        # would this work on Windows? Do I care????
        font_options = [x for x in subprocess.getoutput('ls fonts').split() if x.endswith('tf')]

        for a in self.phrases:
            # make an image out of the text in each entry
            # make its size a multiple of the chop_sizes
            font = ImageFont.truetype(font=random.choice(font_options), size=48, encoding='unic')
            text = a.get()
            text_width, text_height = font.getsize(text)
            if text_width % self.chop_width.get() != 0:
                text_width += (self.chop_width.get() - (text_width % self.chop_width.get()))
            if text_height % self.chop_height.get() != 0:
                text_height += (self.chop_height.get() - (text_height % self.chop_height.get()))
            canvas = Image.new('L', (text_width, text_height), "white")
            draw = ImageDraw.Draw(canvas)
            draw.text((0, 0), text, 'black', font)

            # if user wanted it colorized, colorize it in the most random way possible
            if self.colorized.get():
                text_color = (random.choice(range(255)), random.choice(range(255)), random.choice(range(255)))
                background_color = (random.choice(range(255)), random.choice(range(255)), random.choice(range(255)))
                mid = (random.choice(range(255)), random.choice(range(255)), random.choice(range(255)))
                midpoint = random.choice(range(84, 170))
                blackpoint = random.choice(range(0, 42))
                whitepoint = random.choice(range(212, 255))
                canvas = ImageOps.colorize(canvas, text_color, background_color, mid, blackpoint, whitepoint, midpoint)
    
            # chop the image of the text up into bite-sized blocks
            img_width, img_height = canvas.size
            blocks = []
            for w in range(0, img_width, self.chop_width.get()):
                for h in range(0, img_height, self.chop_height.get()):
                    # are the elif, else conditions still necessary now that original canvas size is modified?
                    if (w + self.chop_width.get() < img_width) and (h + self.chop_height.get() < img_height):
                        box = (w, h, w+self.chop_width.get(), h+self.chop_height.get())
                    elif (w + self.chop_width.get() < img_width) and (h + self.chop_height.get() >= img_height):
                        box = (w, h, w+self.chop_width.get(), img_height)
                    elif (w + self.chop_width.get() >= img_width) and (h + self.chop_height.get() < img_height):
                        box = (w, h, img_width, h+self.chop_height.get())
                    else:
                        box = (w, h, img_width, img_height)
                    blocks.append(canvas.crop(box))
            
            # prepare the new image
            if factors.factor_combinations(len(blocks))[-1][1] > (3 * factors.factor_combinations(len(blocks))[-1][0]):
                sigil_width = math.ceil(math.sqrt(len(blocks))) * self.chop_width.get()
                sigil_height = math.ceil(math.sqrt(len(blocks))) * self.chop_height.get()
                blanks = (math.ceil(math.sqrt(len(blocks))) ** 2) - len(blocks) + 1
                for x in range(1, blanks):
                    blocks.append(Image.new('RGB', (self.chop_width.get(), self.chop_height.get()), color=background_color))
            else:
                sigil_width = factors.factor_combinations(len(blocks))[-1][0] * self.chop_width.get()
                sigil_height = factors.factor_combinations(len(blocks))[-1][1] * self.chop_height.get()
            x, y = 0, 0
            position = (x, y)
            sigil = Image.new('RGB', (sigil_width, sigil_height), 'white')

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

            # save and display
            sigil.save(''.join([str(ord(x)) for x in text[-4:]]) + '.png', 'PNG')
            sigil.show()
            

if __name__ == '__main__':
    gui = Gui()
    gui.root.mainloop()