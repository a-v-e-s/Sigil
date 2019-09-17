import os


def make(img, phrase, show=0, dir=os.getcwd()):
    # save and display the img:
    img.save(os.path.join(dir, hex(hash(phrase))[2:] + '.png'), 'PNG')
    if show == 1:
        img.show()