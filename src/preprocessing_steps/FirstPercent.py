import pandas
import numpy as np
from arch import Hasher, Step

class FirstPercent(Step):
    def __init__(self, percent):

        if percent < 0.0 or percent > 1.0:
            raise Exception(f'Invalid percentage in {self.__class__.__name__}: {percent}')

        self.percent = percent

    def __str__(self) -> str:
        return f'FirstPercent({self.percent})'

    def description(self) -> str:
        return f'Selects the first {self.percent * 100.0}% of images. Depends on IndexToRange and CreateFrameCountColumn.'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:

        # cumsum = data[cols.FRAME_COUNT].cumsum()
        # total_images = int(cumsum.iloc[len(cumsum)-1])

        # count_to_return = np.min([np.rint(total_images * self.percent), total_images])

        # if (count_to_return == 0):
        #     return pandas.DataFrame(columns = data.columns)
       
        # ret = data.loc[cumsum < count_to_return].copy(deep=True)

        # temp = len(ret) # index of split row
        # so_far = 0 if temp == 0 else cumsum.iloc[temp-1]
        # remaining = count_to_return - so_far

        # split_line = data.iloc[temp].copy(deep=True)
        # range = split_line[cols.FRAME_RANGE].copy()
        # range[1] = int(range[0] + remaining - 1)
        # split_line[cols.FRAME_RANGE] = range
        # split_line[cols.FRAME_COUNT] = int(remaining)

        # ret = ret.append(split_line)

        return data

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.percent)
