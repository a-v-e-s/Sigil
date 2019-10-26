import os


def make(phrases, mode, colorized=0, show=0, dir=os.getcwd()):
    if mode == 1:
        from chaos import scramble
        imgs = scramble(phrases, colorized=1)
        #
        for img, phrase in imgs:
            img.save(os.path.join(dir, hex(hash(phrase))[2:] + '.png'), 'PNG')
            if show:
                img.show()
    #
    elif mode == 2:
        import rorshach
        imgs = rorshach.gen_grid(phrases, width=50, height=50)
        for x in imgs:
            x[0].save(os.path.join(dir, hex(hash(x[4]))[2:] + '.png'), 'PNG')
            x[1].save(os.path.join(dir, hex(hash(x[4]))[2:] + '.smoothed.png'), 'PNG')
            x[2].save(os.path.join(dir, hex(hash(x[4]))[2:] + '.smoother.png'), 'PNG')
            x[3].save(os.path.join(dir, hex(hash(x[4]))[2:] + '.smoothest.png'), 'PNG')
            if show:
                x[0].show()
                x[1].show()
                x[2].show()
                x[3].show()
        os.remove('grids.pkl')