import numpy as np

from .BaseLoader import BaseLoader
from helpers import Hasher

class MaskedLoader(BaseLoader):

    def __init__(self, rows=None, columns=None):
        super().__init__(rows, columns)

    def Load(self, file: str) -> np.ndarray:
        img = super().Load(file)
        hh, ww = img.shape[:2]
        print(hh,' ',ww)
        hh2 = int(hh // 2)
        ww2 = int(ww // 2)

        # define circles
        radius = hh2
        yc = hh2
        xc = ww2

        # draw filled circle in white on black background as mask
        mask = np.zeros_like(img) 
        mask = cv2.circle(mask, (xc,yc), int(radius/1.2), (1,1,1), -1)
        # apply mask to image
        img = img* mask

        return img

    def __str__(self) -> str:
        return f'MaskedLoader({self.rows}x{self.columns})'

    def description(self) -> str:
        return "Loads the image from disk as grayscale in the range [0,1] and resizes it to {self.rows} rows by {self.columns} columns, then apply a circular mask to leave only the fetus in the data."

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__)