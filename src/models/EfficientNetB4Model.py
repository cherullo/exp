from tensorflow.keras.optimizers import Adam
from efficientnet.tfkeras import EfficientNetB4
from base.Base import Base

class EfficientNetB4Model(Base):
    def __init__(self, rows=None, columns=None):
        if rows is None:
            rows = 292

        if columns is None:
            columns = 348

        self.rows = rows
        self.columns = columns
        self.loss = 'categorical_crossentropy'
        self.learning_rate = 0.001

    def get(self):
        return self.model

    def compile(self, classes: int = 4):
        self.model = EfficientNetB4(weights=None, input_shape=(self.rows, self.columns, 3), classes=classes)

        optimizer = Adam(learning_rate=self.learning_rate)
        self.model.compile(loss=self.loss, optimizer=optimizer, metrics=['acc'])
       
    def ToString(self):
        return f'EfficientNetB4[loss={self.loss}, optimizer=Adam(learning_rate={self.learning_rate})]'

    def Description(self):
        return f'EfficientNetB4 model'

    def AddHash(self, h):
        return h.ordered(self.__class__.__name__, self.loss, 'adam', self.learning_rate)
