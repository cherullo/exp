import numpy as np

import skimage.io as io
from skimage.util import img_as_float32
from skimage.transform import resize

from arch import Base
from arch import Hasher

class BaseLoader(Base):
    """ 
        Loads an image and optionally resizes it.
    """
    def __init__(self, resize: tuple[int, int] = None):
        self.resize = resize

    def load(self, file: str) -> np.ndarray:
        """ Loads an image.

        Args:
            file (str): Image file path.

        Returns:
            np.ndarray: The image ndarray.
        """
        img = img_as_float32(io.imread(file)) * 255.0

        if self.resize != None:
            img = resize(img, (self.resize[0], self.resize[1]), anti_aliasing=True)
    
        return img

    def __str__(self) -> str:
        return f'BaseLoader(resize={self.resize})'

    def description(self) -> str:
        resizeStr = f' and resizes it to {self.resize[0]} rows by {self.resize[1]} columns.' if self.resize is not None else ''

        return f'Loads the image from disk with values in the range [0, 255]{resizeStr}'

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__)
