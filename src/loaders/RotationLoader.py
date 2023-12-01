import random
import numpy as np
from skimage.transform import rotate
from .BaseLoader import BaseLoader
from arch import Hasher

class RotationLoader(BaseLoader):
    def __init__(self, angle=0.0, spread=0.0, resize: tuple[int, int] = None):
        super().__init__(resize)
        self.angle = angle
        self.spread = spread

    def load(self, file: str) -> np.ndarray:
        """ Loads an image and rotates it.

        Args:
            file (str): Image file path.

        Returns:
            np.ndarray: The image ndarray.
        """
        img = super().load(file)

        angle = self.angle + random.uniform(-1.0, 1.0) * self.spread
        return rotate(img, angle)

    def __str__(self) -> str:
        return f'RotationLoader(angle={self.angle}, spread={self.spread}, resize={self.resize})'

    def description(self) -> str:
        return f'{super().description()} and then rotates by {self.angle} +- {self.spread} degrees.'

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.angle, self.spread)


