import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from efficientnet.tfkeras import EfficientNetB4

from arch import BaseModel

class EfficientNetB4Model(BaseModel):
    def __init__(self):
        self.loss = 'categorical_crossentropy'
        self.learning_rate = 0.001

    def get(self) -> tf.keras.Model:
        return self.model

    def compile(self, classes: int = 4):
        self.model = EfficientNetB4(weights=None, classes=classes)

        optimizer = Adam(learning_rate=self.learning_rate)
        self.model.compile(loss=self.loss, optimizer=optimizer, metrics=['acc'])
       
    def __str__(self):
        return f'EfficientNetB4[loss={self.loss}, optimizer=Adam(learning_rate={self.learning_rate})]'

    def description(self):
        return f'EfficientNetB4 model'

    def add_hash(self, h):
        return h.ordered(self.__class__.__name__, self.loss, 'adam', self.learning_rate)
