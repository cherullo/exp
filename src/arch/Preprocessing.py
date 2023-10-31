from typing import List
import numpy as np

import pandas

from arch import Base, Step

class Preprocessing(Base):
    def __init__(self):
        self._steps: List[Step] = []

    def __str__(self):
        return self.description()

    def add_step(self, step: Step):
        self._steps.append(step)

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        for step in self._steps:
            data = step.process(data)

        return data

    def description(self) -> str:
        col1 = [str(x) for x in self._steps]
        col1_width = np.max([len(x) for x in col1]) + 3
        col2 = [x.description() for x in self._steps]

        ret = ""
        for col1, col2 in zip(col1, col2):
            ret = ret + ' ' + col1.ljust(col1_width) + col2 + "\n"
        
        return ret

    def add_hash(self, hasher):
        hasher.ordered(*self._steps)