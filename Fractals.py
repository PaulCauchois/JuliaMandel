# Créé par Paul Cauchois, licence CC-BY 4.0
from PIL import Image as im
import numpy as np


def Sierpinski_Carpet(n):
    Start = im.fromarray(np.array([0]), mode="1")
    new = Start.copy()
    for i in range(n):
        old = new.copy()
        new = im.new(mode="1", size=tuple(3 * np.array(old.size)), color=1)
        for i in range(3):
            for j in range(3):
                if i != 1 or j != 1:  # Don't paste in the middle
                    new.paste(old, (i * old.width, j * old.height))
    return new


Sierpinski_Carpet(8).save("Sierpinski Carpet t.png")
