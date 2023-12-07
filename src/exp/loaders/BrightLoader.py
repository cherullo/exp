import numpy as np

from exp.arch import Hasher
from .SimpleLoader import SimpleLoader

class BrightLoader(SimpleLoader):

    def __init__(self, alpha: float = 1.0, beta: float = 0.0, resize: tuple[int, int] = None):
        super().__init__(resize)
        self.alpha = alpha
        self.beta = beta

    def load(self, file: str) -> np.ndarray:
        """ Loads an image and adjusts its brightness.

        Args:
            file (str): Image file path.

        Returns:
            np.ndarray: The image ndarray.
        """
        img = super().load(file)
        
        img = (img * self.alpha) + self.beta

        return np.clip(img, 0, 255)

    def __str__(self) -> str:
        return f'BrightLoader(alpha={self.alpha}, beta={self.beta}, resize={self.resize})'

    def description(self) -> str:
        return f'{super().description()} and then multiplies each pixel by {self.alpha} and then adds {self.beta}.'

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.alpha, self.beta)
