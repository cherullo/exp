import pandas
import numpy as np
import annotations.columns as cols
from arch import Hasher, Step

class CreateFrameCountColumn(Step):

    def __init__(self):
        pass

    def ToString(self) -> str:
        return 'CreateFrameCountColumn'

    def Description(self) -> str:
        return 'Creates the \'frameCount\' column with the number of frames defined in each row with label View. Depends on ParseRange.'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:

        column_count = len(data.columns)
        data.insert(column_count, cols.FRAME_COUNT, np.zeros(len(data)))

        is_frame_label = (data[cols.ANNOTATION_TYPE] == 'frame_label')
        has_frame_index = pandas.notna(data[cols.FRAME_INDEX])
        data.loc[is_frame_label & has_frame_index, cols.FRAME_COUNT] = 1

        is_frame_range_label = (data[cols.ANNOTATION_TYPE] == 'frame_range_label')
        has_frame_range = pandas.notna(data[cols.FRAME_RANGE])

        range_rows = is_frame_range_label & has_frame_range
        temp = [ int(x[1] - x[0] + 1) for x in data.loc[range_rows, cols.FRAME_RANGE]]
        data.loc[range_rows, cols.FRAME_COUNT] = temp

        return data

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__)





