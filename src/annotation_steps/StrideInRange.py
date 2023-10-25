import pandas
import numpy as np
import annotations.columns as cols
from .BaseFilter import BaseFilter
from helpers.Hasher import Hasher

class StrideInRange(BaseFilter):
    def __init__(self, stride):
        self.stride = stride

    def ToString(self) -> str:
        return f'StrideInRange({self.stride})'

    def Description(self) -> str:
        return f'Selects one frame every {self.stride} frames in frame_range_label rows. Keeps all other rows intact. Depends on ParseRange.'

    def ProcessStep(self, data: pandas.DataFrame) -> pandas.DataFrame:

        new_rows = []

        for _, row in data.iterrows():
            if (row[cols.ANNOTATION_TYPE] != 'frame_range_label'):
                new_row = row.copy(deep=True)
                new_rows.append(new_row)
                continue

            frame_range = row[cols.FRAME_RANGE]

            for frame_index in range(frame_range[0], frame_range[1] + 1, self.stride):
                new_row = row.copy(deep=True)
                new_row[cols.FRAME_COUNT] = 1
                new_row[cols.FRAME_RANGE] = [frame_index, frame_index]
                new_rows.append(new_row)

        return pandas.DataFrame(data=new_rows, columns=data.columns)

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.stride)