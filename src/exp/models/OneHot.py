import numpy as np
from tensorflow.keras.utils import to_categorical
from exp.arch import Base

class OneHot(Base):
    """Class receives a panda.Series object 
    and return one hot numpy array."""
    def __init__(self, labels):
        self.labels = labels # We should duplicate this array
        
        self.labels2Y = dict(zip(self.labels, to_categorical(range(0, len(self.labels)))))

    def encode(self, target):
        if (isinstance(target, str)):
            return self.labels2Y[target]

        return [self.labels2Y[item] for item in target]

    def decode(self, pred):
        index = np.argmax(pred)
        return self.labels[index]

    def __str__(self) -> str:
        temp = ', '.join(self.labels)
        weights_str = '1'
        return f'OneHot([{temp}], [{weights_str}])'

    def description(self) -> str:
        temp = ', '.join(self.labels)
        return f'One-hot encodes the labels {temp}.'

    def add_hash(self, h):
        h.ordered(self.__class__.__name__).ordered(*self.labels)