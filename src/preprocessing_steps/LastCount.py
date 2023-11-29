import pandas
import numpy as np
from arch import Hasher, Step

class LastCount(Step):
    def __init__(self, count):
        self.count = int(np.abs(count))

    def __str__(self) -> str:
        return f'LastCount({self.count})'

    def description(self) -> str:
        return f'Selects the last {self.count} images. Depends on IndexToRange and CreateFrameCountColumn.'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:

        # if len(data) == 0:
        #     return data

        # cumsum = data[cols.FRAME_COUNT].cumsum()
        # total_images = cumsum.iloc[len(cumsum)-1]

        # count_to_return = int(np.min([self.count, total_images]))

        # if (count_to_return == 0):
        #     return pandas.DataFrame(columns = data.columns)

        # if (count_to_return == total_images):
        #     return data
       
        # ret = data.loc[cumsum > total_images - count_to_return].copy(deep=True)

        # temp = len(data) - len(ret) # index of split row
        # needed = cumsum.iloc[temp] - (total_images - count_to_return)

        # split_line = ret.iloc[0].copy(deep=True)
        # excess = split_line[cols.FRAME_COUNT] - needed

        # range = split_line[cols.FRAME_RANGE].copy()
        # range[0] = int(range[1] - needed + 1)
        # split_line[cols.FRAME_RANGE] = range

        # split_line[cols.FRAME_COUNT] = int(needed)
        # ret.iloc[0] = split_line

        return data

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.count)
