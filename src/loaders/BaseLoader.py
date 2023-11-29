import numpy as np

import skimage.io as io
from skimage.util import img_as_float32
from skimage.transform import resize

from arch import Base
from arch import Hasher

class BaseLoader(Base):
    def __init__(self, resize: tuple[int, int] = None):
        self.resize = resize

    def load(self, file: str) -> np.ndarray:
        img = img_as_float32(io.imread(file))

        if (self.resize != None):
            img = resize(img, (self.resize[0], self.resize[1]), anti_aliasing=True)
    
        return img

    def __str__(self) -> str:
        return f'BaseLoader({self.rows}x{self.columns})'

    def description(self) -> str:
        return "Loads the image from disk as grayscale in the range [0,1] and resizes it to {self.rows} rows by {self.columns} columns."

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__)
