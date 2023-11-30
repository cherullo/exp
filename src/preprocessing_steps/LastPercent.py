import pandas
import numpy as np
from arch import Hasher, Step

class LastPercent(Step):
    def __init__(self, percent):

        if percent < 0.0 or percent > 1.0:
            raise Exception(f'Invalid percentage in {self.__class__.__name__}: {percent}')

        self.percent = percent

    def __str__(self) -> str:
        return f'LastPercent({self.percent})'

    def description(self) -> str:
        return f'Selects the last {self.percent * 100.0}% of images. Depends on CreateFrameCountColumn and ParseRange.'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        if len(data) == 0:
            return data

        total_rows = len(data.index)

        count_to_return = int(self.percent * total_rows)

        return data[count_to_return:]

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.percent)
