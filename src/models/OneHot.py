import numpy as np
from tensorflow.keras.utils import to_categorical
from base.Base import Base
import annotations.severities as sevs

class OneHot(Base):
    """Class receives a panda.Series object 
    and return one hot numpy array."""
    def __init__(self, labels=None, weights=None):
        self.labels = labels
        if self.labels is None:
            self.labels = [sevs.THREEVT, sevs.THREEVV, sevs.FOURCH, sevs.LVOT, sevs.RVOT]

        self.weights = weights
        if self.weights is None:
            self.weights = np.ones(len(self.labels))

        self.labels2Y = dict(zip(self.labels, to_categorical(range(0, len(self.labels)))))

    def encode(self, target):
        if (isinstance(target, str)):
            return self.labels2Y[target]

        return [self.labels2Y[item] for item in target]

    def decode(self, pred):
        index = np.argmax(pred)
        return self.labels[index]

    def ToString(self) -> str:
        temp = ', '.join(self.labels)
        weights_str = ', '.join([str(x) for x in self.weights])
        return f'OneHot([{temp}], [{weights_str}]'

    def Description(self) -> str:
        temp = ', '.join(self.labels)
        weights_str = ', '.join([str(x) for x in self.weights])
        return f'One-hot encodes the labels {temp} with weights {weights_str}.'

    def AddHash(self, h):
        h.ordered(self.__class__.__name__).ordered(*self.labels).ordered(*self.weights)