import random
import numpy as np
from skimage.transform import rotate
from .BaseLoader import BaseLoader
from arch import Hasher

class RotationLoader(BaseLoader):
    def __init__(self, angle=10.0, spread=0.0, resize: tuple[int, int] = None):
        super().__init__(resize)
        self.angle = angle
        self.spread = spread

    def load(self, file: str) -> np.ndarray:
        img = super().load(file)

        angle = self.angle + random.uniform(-1.0, 1.0) * self.spread
        return rotate(img, angle)

    def __str__(self) -> str:
        spread_txt = f', spread={self.spread}' if self.spread != 0.0 else ''
        return f'RotationLoader(angle={self.angle}{spread_txt})'

    def description(self) -> str:
        resizeStr = ''
        if (self.resize):
            resizeStr = f', resizes it to {self.resize[0]} rows by {self.resize[1]} columns'

        return f'Loads the image from disk{resizeStr} and then rotates by {self.angle} +- {self.spread} degrees.'

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.angle, self.spread)


