import numpy as np
import random
from skimage.transform import rotate
from .BaseLoader import BaseLoader
from helpers import Hasher


class RotationLoader(BaseLoader):

    def __init__(self, angle=10.0, spread=0.0, rows=None, columns=None):
        super().__init__(rows, columns)
        self.angle = angle
        self.spread = spread

    def Load(self, file: str) -> np.ndarray:
        img = super().Load(file)

        angle = self.angle + random.uniform(-1.0, 1.0) * self.spread
        return rotate(img, angle)

    def ToString(self) -> str:
        spread_txt = f', spread={self.spread}' if self.spread != 0.0 else ''
        return f'RotationLoader(angle={self.angle}{spread_txt})'

    def Description(self) -> str:
        return f'Loads the image from disk as grayscale in the range [0,1], resizes it to {self.rows} rows by {self.columns} columns and then rotates by {self.angle} +- {self.spread} degrees.'

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.angle, self.spread)


