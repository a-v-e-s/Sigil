"""
make.py

takes input from gui.py and sends it to the appropriate module
"""

import os

def make(phrases, mode, colorized=0, blur=0, show=0, dir=os.getcwd()):
    # chaos mode:
    if mode == 1:
        import chaos
        imgs = chaos.scramble(phrases, colorized=1, chop_width=10, chop_height=10)
    # rorshach mode:
    elif mode == 2:
        import rorshach
        imgs = rorshach.gen_grid(phrases, blur=0, width=480, height=360)
    #
    # save and display the image if the user requested:
    for img, phrase in imgs:
        img.save(os.path.join(dir, hex(hash(phrase))[2:] + '.png'), 'PNG')
        if show:
            img.show()
    try:
        os.remove('grids.pkl')
    except FileNotFoundError:
        pass