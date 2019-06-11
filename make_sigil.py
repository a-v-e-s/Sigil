"""
make_sigil.py:

Author: Jon David Tannehill
"""

from PIL import Image, ImageFont, ImageDraw, ImageOps
import tkinter as tk
import subprocess, sys, random, math

"""
PIL
"Effects": Reduce Noice, Spread, Edge Detect, 
"FX": Swirl, Implode, Oil Paint
Add better colorization?
Fix block/position issue
"""

class Gui():
    def __init__(self):
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

        self.add_entry()
        self.add_entry()
        d.set(10)
        f.set(10)
        h.deselect()

        self.font_options = [x for x in subprocess.getoutput('ls fonts').split() if x.endswith('tf')]
        self.chop_width.set(10)
        self.chop_height.set(10)
        self.entries[0].focus_set()
        
        self.root.bind(sequence='<Return>', func=(lambda x=self.make_sigil: self.make_sigil()))
        self.root.bind(sequence='<Control-KeyPress-n>', func=(lambda y=self.add_entry: self.add_entry()))
        self.root.bind(sequence='<Control-KeyPress-d>', func=(lambda z=self.remove: self.remove()))


    def add_entry(self):
        text = tk.StringVar()
        entry = tk.Entry(self.root, width=40, textvariable=text)
        entry.grid(row=self.rownum-6, column=1, columnspan=2)
        self.phrases.append(text)
        self.entries.append(entry)
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
        del self.phrases[-1]
        self.entries[-1].grid_forget()
        del self.entries[-1]

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
        for a in self.phrases:
            font = ImageFont.truetype(font=random.choice(self.font_options), size=48, encoding='unic')
            text = a.get()
            text_width, text_height = font.getsize(text)
            canvas = Image.new('L', (text_width, text_height), "white")
            draw = ImageDraw.Draw(canvas)
            draw.text((0, 0), text, 'black', font)

            if self.colorized.get():
                text_color = (random.choice(range(255)), random.choice(range(255)), random.choice(range(255)))
                background_color = (random.choice(range(255)), random.choice(range(255)), random.choice(range(255)))
                mid = (random.choice(range(255)), random.choice(range(255)), random.choice(range(255)))
                midpoint = random.choice(range(255))
                blackpoint = random.choice(range(0, midpoint))
                whitepoint = random.choice(range(midpoint, 255))
                canvas = ImageOps.colorize(canvas, text_color, background_color, mid, blackpoint, whitepoint, midpoint)
    
            img_width, img_height = canvas.size
            blocks = []
            for w in range(0, img_width, self.chop_width.get()):
                for h in range(0, img_height, self.chop_height.get()):
                    box = (w, h, w+self.chop_width.get(), h+self.chop_height.get())
                    blocks.append(canvas.crop(box))
            
            sigil_width = math.ceil(math.sqrt(len(blocks))) * self.chop_width.get()
            sigil_height = math.ceil(math.sqrt(len(blocks))) * self.chop_height.get()
            x, y = 0, sigil_height
            position = (x, y)
            random.shuffle(blocks)
            sigil = Image.new('RGB', (sigil_width, sigil_height), 'white')

            for b in blocks:
                sigil.paste(b, box=position)
                if (position[0] + self.chop_width.get()) <= sigil_width:
                    x += self.chop_width.get()
                else:
                    x = 0
                    y -= self.chop_height.get()
                position = (x, y)

            sigil.save(''.join([str(ord(x)) for x in text[:4]]) + '.png', 'PNG')
            sigil.show()
            

if __name__ == '__main__':
    gui = Gui()
    gui.root.mainloop()