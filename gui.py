import tkinter as tk
from tkinter.filedialog import askdirectory
from make import make
import os


class Gui():
    def __init__(self):
        # initialize the widgets, variables, etc.
        self.root = tk.Tk()
        self.root.title('Image Maker')
        tk.Label(self.root, text='Enter the text you wish to turn into'
            'an image:').grid(row=1, column=1, columnspan=2)
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
        z.configure(text='Go!', command=make)
        z.grid(row=self.rownum, column=1, columnspan=2)

        # add room for two statements, and set the options to defaults
        self.add_entry()
        self.add_entry()
        d.deselect()
        f.deselect()
        self.entries[0].focus_set()
        
        # keybindings
        self.root.bind(sequence='<Return>', func=(lambda
            x=make: make()))
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


if __name__ == '__main__':
    gui = Gui()
    gui.root.mainloop()