import tensorflow as tf
import pandas
import numpy as np

from .Base import Base
import arch.dataset_columns as cols

class DatasetGenerator(Base, tf.keras.utils.Sequence):
    def __init__(self,
                 dataset: pandas.DataFrame=None,
                 encoding=None,
                 batch_size = 12,
                 shuffle = True):
                
        self.dataset = dataset
        self.encoding = encoding
        self.batch_size = batch_size
        self.shuffle = shuffle
    
    def __len__(self):
        return int(np.ceil( len(self.dataset) / self.batch_size ))
    
    def __getitem__(self, idx):
        
        bs = self.batch_size
        base_idx = idx * bs
        rows = self.dataset[base_idx : base_idx+bs]

        X = [ row[cols.INPUT_LOADER].load(row[cols.INPUT]) for _,row in rows.iterrows() ]

        X = np.array(X)
        y = np.array(self.encoding.encode(rows[cols.OUTPUT]))

        return X, y

    def on_epoch_end(self):
        self.dataset = self.dataset.sample(frac=1).reset_index(drop=True)

    def __str__(self) -> str:
        return f'DatasetGenerator(batch_size={self.batch_size}, shuffle={self.shuffle})'

    def description(self) -> str:
        return f'Default DatasetGenerator with batch_size={self.batch_size} and shuffle={self.shuffle}'

    def add_hash(self, h):
        h.ordered(self.batch_size, self.shuffle)