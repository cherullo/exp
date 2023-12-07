from abc import abstractmethod
import tensorflow as tf

from .Base import Base

class BaseModel(Base):
    """ 
    A neural network model.

    Args:
        Base (_type_): This is a hashable type.
    """

    @abstractmethod
    def get(self) -> tf.keras.Model:
        """ 
        Returns the compiled Keras neural network model.
        """
        pass

    @abstractmethod
    def compile(self, classes: int = 4):
        """
        Compiles the Keras neural network model.

        Args:
            classes (int, optional): The number of classification classes. Defaults to 4.
        """
        pass