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
        imgs = rorshach.gen_grid(phrases, width=480, height=360)
        for img, smoothed, smoother, smoothest, phrase in imgs:
            img.save(os.path.join(dir, hex(hash(phrase))[2:] + '.png'), 'PNG')
            smoothed.save(os.path.join(dir, hex(hash(phrase))[2:] + '.smoothed.png'), 'PNG')
            smoother.save(os.path.join(dir, hex(hash(phrase))[2:] + '.smoother.png'), 'PNG')
            smoothest.save(os.path.join(dir, hex(hash(phrase))[2:] + '.smoothest.png'), 'PNG')
            if show:
                img.show()
                smoothed.show()
                smoother.show()