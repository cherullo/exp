from tensorflow.keras.optimizers import Adam
from efficientnet.tfkeras import EfficientNetB0
from arch import Base

class EfficientNetB0Model(Base):
    def __init__(self):

        self.loss = 'categorical_crossentropy'
        self.learning_rate = 0.001

    def get(self):
        return self.model

    def compile(self, classes: int = 4):
        self.model = EfficientNetB0(weights=None, input_shape=(292, 348, 1), classes=classes)

        optimizer = Adam(learning_rate=self.learning_rate)
        self.model.compile(loss=self.loss, optimizer=optimizer, metrics=['acc'])
       
    def __str__(self):
        return f'EfficientNetB0[loss={self.loss}, optimizer=Adam(learning_rate={self.learning_rate})]'

    def description(self):
        return f'EfficientNetB0 model'

    def add_hash(self, h):
        return h.ordered(self.__class__.__name__, self.loss, 'adam', self.learning_rate)
