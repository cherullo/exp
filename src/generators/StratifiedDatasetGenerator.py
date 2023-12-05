from typing import Dict

import pandas
import numpy as np

from arch import BaseDatasetGenerator
import arch.dataset_columns as cols

class StratifiedDatasetGenerator(BaseDatasetGenerator):
    def __init__(self,
                 dataset: pandas.DataFrame=None,
                 encoding=None,
                 samples_per_class=500,
                 seed=42,
                 batch_size = 16,
                 shuffle = True):
        
        self.dataset = dataset
        self.encoding = encoding
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.samples_per_class: int = samples_per_class
        self.seed = seed

        self._epoch=0
        self._dataset_per_class: Dict[str, pandas.DataFrame] = None
        self.epoch_dataset: pandas.DataFrame = None
            
    def __len__(self):
        dataset_per_class = self._get_dataset_per_class()

        samples_per_epoch = 0
        for label, class_dataset in dataset_per_class.items():
            samples_per_epoch += min(self.samples_per_class, len(class_dataset))

        return int(np.ceil(samples_per_epoch / self.batch_size))
    
    def _get_dataset_per_class(self):
        if self._dataset_per_class is None:

            temp:Dict[str, pandas.DataFrame]=dict()

            for label in self.encoding.labels:
                temp[label] = self.dataset.loc[self.dataset[cols.LABEL] == label]

            self._dataset_per_class=temp

        return self._dataset_per_class

    def generate_epoch_dataset(self):

        dataset_per_class = self._get_dataset_per_class()
        pieces=[]

        for index, (label, class_dataset) in enumerate(dataset_per_class.items()):
            to_sample=min(len(class_dataset), self.samples_per_class)
            random_state = self.seed + 5*self._epoch + 7*index
            pieces.append(class_dataset.sample(n=to_sample, random_state=random_state))

        ret: pandas.DataFrame = pandas.concat(pieces, ignore_index=True, copy=True)

        if self.shuffle is True:
            ret = ret.sample(frac=1).reset_index(drop=True)

        return ret

    def __getitem__(self, idx):
        
        if self.epoch_dataset is None:
            self.epoch_dataset = self.generate_epoch_dataset()

        bs = self.batch_size
        base_idx = idx * bs
        rows = self.epoch_dataset[base_idx : base_idx+bs]

        X = [ row[cols.LOADER].Load(row[cols.INPUT]) for _,row in rows.iterrows() ]

        X = np.array(X)
        y = np.array(self.encoding.encode(rows[cols.LABEL]))

        return X, y

    def on_epoch_end(self):
        self._epoch += 1
        self.epoch_dataset = self.generate_epoch_dataset()

    def __str__(self) -> str:
        return f'StratifiedDatasetGenerator(samples_per_class={self.samples_per_class}, seed={self.seed}, batch_size={self.batch_size}, shuffle={self.shuffle})'

    def description(self) -> str:
        return f'Stratified Dataset Generator which takes {self.samples_per_class} sampler per class each epoch, using seed={self.seed}, batch_size={self.batch_size} and shuffle={self.shuffle}'

    def add_hash(self, h):
        h.ordered('StratifiedDatasetGenerator', self.samples_per_class, self.seed, self.batch_size, self.shuffle)