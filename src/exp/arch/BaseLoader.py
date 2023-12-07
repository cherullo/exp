import numpy as np

from .Base import Base

class BaseLoader(Base):
    """
    Abstract class for all image loaders.

    Args:
        Base (_type_): This is a hashable type.
    """
    def load(self, file: str) -> np.ndarray:
        """ Loads an image.

        Args:
            file (str): Image file path.

        Returns:
            np.ndarray: The image ndarray.
        """
        pass