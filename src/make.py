"""
make.py:
Takes input from gui.py and sends it to the appropriate module.
Saves and optionally displays the results.
"""

import os

def make(phrases, mode, colorized=1, blur=0, show=1, dir=os.getcwd()):
    # chaos mode:
    if mode == 1:
        import chaos
        imgs = chaos.scramble(phrases, colorized=1, chop_width=10, chop_height=10)
    # rorshach mode:
    elif mode == 2:
        import rorshach
        imgs = rorshach.gen_grid(phrases, colorized=1, blur=0, width=360, height=360)
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