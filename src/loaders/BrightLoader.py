import numpy as np

from .BaseLoader import BaseLoader
from arch import Hasher

class BrightLoader(BaseLoader):

    def __init__(self, alpha=1.0, beta=0.0, resize: tuple[int, int] = None):
        super().__init__(resize)
        self.alpha = alpha
        self.beta = beta

    def load(self, file: str) -> np.ndarray:
        img = super().Load(file)
        
        img = (img * self.alpha) + self.beta

        return np.clip(img, 0, 1)

    def __str__(self) -> str:
        alpha_str = f'{self.alpha} * ' if self.alpha != 1.0 else ''
        beta_str = f' + {self.beta}' if self.beta != 0.0 else ''

        return f'BrightLoader({alpha_str}X{beta_str})'

    def description(self) -> str:
        return f'Loads the image from disk as grayscale in the range [0,1], resizes it to {self.rows} rows by {self.columns} columns and then multiplies each pixel by {self.alpha} and then adds {self.beta}.'

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.alpha, self.beta)
