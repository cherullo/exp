import pandas
import numpy as np
import annotations.columns as cols
from arch import Hasher, Step

class FirstCount(Step):
    def __init__(self, count):
        self.count = int(np.abs(count))

    def ToString(self) -> str:
        return f'FirstCount({self.count})'

    def Description(self) -> str:
        return f'Selects the first {self.count} images. Depends on IndexToRange and CreateFrameCountColumn.'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:

        if len(data) == 0:
            return data

        cumsum = data[cols.FRAME_COUNT].cumsum()
        total_images = cumsum.iloc[len(cumsum)-1]

        count_to_return = int(np.min([self.count, total_images]))

        if (count_to_return == 0):
            return pandas.DataFrame(columns = data.columns)

        if (count_to_return == total_images):
            return data
       
        ret = data.loc[cumsum < count_to_return].copy(deep=True)

        temp = len(ret) # index of split row
        so_far = 0 if temp == 0 else cumsum.iloc[temp-1]
        remaining = count_to_return - so_far

        split_line = data.iloc[temp].copy(deep=True)
        range = split_line[cols.FRAME_RANGE].copy()
        range[1] = int(range[0] + remaining - 1)
        split_line[cols.FRAME_RANGE] = range
        split_line[cols.FRAME_COUNT] = int(remaining)

        ret = ret.append(split_line)

        return ret

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.count)