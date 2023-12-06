from abc import abstractmethod
import tensorflow as tf
import numpy as np

from .Base import Base

class BaseDatasetGenerator(Base, tf.keras.utils.Sequence):
    """
    Abstract class of all dataset generators.

    Args:
        Base (_type_): This is a framework type.
        tf (_type_): Tensorflow sequence.
    """
    @abstractmethod
    def __len__(self) -> int:
        """
        Returns how many batches are in this dataset.
        """
        pass
    
    @abstractmethod
    def __getitem__(self, index: int):
        """
        Returns the index-th batch in this dataset.

        Args:
            index (int): The batch index.

        Returns:
            (X: np.array, y: np.array): A list of images and a list containing the corresponding encoded labels.
        """
        pass

    @abstractmethod
    def on_epoch_end(self):
        """
        Method called when the epoch ends.
        """
        pass
