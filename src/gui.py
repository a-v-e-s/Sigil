"""
gui.py:
The top-level script for this repository.
Provides a graphical frontend for encoding language into an image
"""

import tkinter as tk
from tkinter.filedialog import askdirectory
from make import make
import os, threading


class Gui():
    def __init__(self):
        # initialize the root widget and its frames:
        self.root = tk.Tk()
        self.root.title('Image Maker')
        self.text = tk.Frame(self.root)
        self.options = tk.Frame(self.root)
        self.operation = tk.Frame(self.root)
        self.text.pack()
        self.options.pack()
        self.operation.pack()
        #
        # fill out the text frame:
        tk.Label(self.text, text='Enter the text you wish to turn into an image:').grid(row=1, column=1, columnspan=2)
        self.rownum = 2
        self.phrases = []
        self.entries = []
        self.add = tk.Button(self.text, text='Add Another', command=self.add_entry)
        self.add.grid(row=self.rownum, column=1)
        self.delete = tk.Button(self.text, text='Delete Previous', command=self.remove)
        self.delete.grid(row=self.rownum, column=2)
        self.add_entry()
        self.add_entry()
        self.reposition()
        self.entries[0].focus_set()
        #
        # fill out the options frame:
        self.mode = tk.IntVar()
        self.colorized = tk.IntVar()
        self.blurring = tk.IntVar()
        self.shown = tk.IntVar()
        tk.Label(self.options, text='Choose Mode:').grid(row=1, column=1, columnspan=3)
        self.rorshach = tk.Radiobutton(self.options, text='Rorshach', variable=self.mode, value=2, command=self.rorsh_mode)
        self.chaos = tk.Radiobutton(self.options, text='Chaos', variable=self.mode, value=1, command=self.chaos_mode)
        self.kaleidoscope = tk.Radiobutton(self.options, text='Kaleidoscope', variable=self.mode, value=3, state='disabled')
        self.chaos.grid(row=2, column=1)
        self.rorshach.grid(row=2, column=2)
        self.kaleidoscope.grid(row=2, column=3)
        self.colorize_l = tk.Label(self.options, text='Colorize:')
        self.colorize = tk.Checkbutton(self.options, variable=self.colorized, offvalue=0, onvalue=1)
        self.colorize_l.grid(row=3, column=1, columnspan=2)
        self.colorize.grid(row=3, column=3)
        self.blur_l = tk.Label(self.options, text='Blur:')
        self.blur = tk.Scale(self.options, variable=self.blurring, orient='horizontal', from_=0, to=3)
        tk.Label(self.options, text='Automatically show resulting image?').grid(row=5, column=1, columnspan=2)
        self.show = tk.Checkbutton(self.options, variable=self.shown, offvalue=0, onvalue=1)
        self.show.grid(row=5, column=3)
        self.mode.set(2)
        self.rorsh_mode()
        #
        # fill out the operation frame:
        self.dir = tk.StringVar()
        tk.Label(self.operation, text='\nChoose folder to save images in or default to:\n' + os.getcwd()).grid(row=1, column=1, columnspan=2)
        self.directory = tk.Entry(self.operation, textvariable=self.dir, width=40)
        self.directory.grid(row=2, column=1)
        self.directory_menu = tk.Button(self.operation, text='Browse', command=(lambda x=self.directory:[x.delete(0, len(x.get())), x.insert(0, askdirectory())]))
        self.directory_menu.grid(row=2, column=2)
        self.start = tk.Button(self.operation, text='Go!', command=self.go)
        self.start.grid(row=3, column=1, columnspan=2)
        #
        # keybindings
        self.root.bind(sequence='<Return>', func=(lambda x: self.go()))
        self.root.bind(sequence='<Control-KeyPress-n>', func=(lambda y=self.add_entry: self.add_entry()))
        self.root.bind(sequence='<Control-KeyPress-d>', func=(lambda z=self.remove: self.remove()))


    def add_entry(self):
        # create new entry widget and variable for it
        text = tk.StringVar()
        entry = tk.Entry(self.text, width=60, textvariable=text)
        entry.grid(row=self.rownum, column=1, columnspan=2)
        self.phrases.append(text)
        self.entries.append(entry)
        #
        # adjust other widgets accordingly
        self.rownum += 1
        self.reposition()

    
    def remove(self):
        # remove the entry widget and its variable
        del self.phrases[-1]
        self.entries[-1].grid_forget()
        del self.entries[-1]
        #
        # adjust widgets accordingly
        self.rownum -= 1
        self.reposition()

    
    def reposition(self):
        # move the add and delete buttons into the proper location:
        self.add.grid(row=self.rownum, column=1)
        self.delete.grid(row=self.rownum, column=2)


    def rorsh_mode(self):
        # adjust options widgets:
        self.blur_l.grid(row=4, column=1, columnspan=2)
        self.blur.grid(row=4, column=3)
        self.blur.configure(state='normal')


    def chaos_mode(self):
        # adjust options widgets:
        self.blurring.set(0)
        self.blur.configure(state='disabled')


    def go(self):
        # append all phrases to a list and start make.make() in its own thread:
        phrases = []
        for x in self.phrases:
            phrases.append(x.get())
        threading.Thread(
            target=make,
            args=(
                phrases,
                self.mode.get(),
                self.colorized.get(),
                self.blurring.get(),
                self.shown.get(),
                self.dir.get()
            )
        ).start()


if __name__ == '__main__':
    # initialize the gui:
    gui = Gui()
    gui.root.mainloop()