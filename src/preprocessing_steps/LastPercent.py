import pandas
import numpy as np
import annotations.columns as cols
from arch import Hasher, Step

class LastPercent(Step):
    def __init__(self, percent):

        if percent < 0.0 or percent > 1.0:
            raise Exception(f'Invalid percentage in {self.__class__.__name__}: {percent}')

        self.percent = percent

    def ToString(self) -> str:
        return f'LastPercent({self.percent})'

    def Description(self) -> str:
        return f'Selects the last {self.percent * 100.0}% of images. Depends on CreateFrameCountColumn and ParseRange.'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:

        cumsum = data[cols.FRAME_COUNT].cumsum()
        total_images = cumsum.iloc[len(cumsum)-1]

        count_to_return = np.min([np.rint(total_images * self.percent), total_images])

        if (count_to_return == 0):
            return pandas.DataFrame(columns = data.columns)
       
        ret = data.loc[cumsum > total_images - count_to_return].copy(deep=True)

        temp = len(data) - len(ret) # index of split row
        needed = cumsum.iloc[temp] - (total_images - count_to_return)

        split_line = ret.iloc[0].copy(deep=True)
        excess = split_line[cols.FRAME_COUNT] - needed

        range = split_line[cols.FRAME_RANGE].copy()
        range[0] = int(range[1] - needed + 1)
        split_line[cols.FRAME_RANGE] = range

        split_line[cols.FRAME_COUNT] = int(needed)
        ret.iloc[0] = split_line

        return ret

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.percent)
