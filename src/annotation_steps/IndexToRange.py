import pandas
import annotations.columns as cols
from helpers import Hasher
from .BaseFilter import BaseFilter

class IndexToRange(BaseFilter):

    def __init__(self):
        pass

    def ToString(self) -> str:
        return "IndexToRange"

    def Description(self) -> str:
        return f'Converts rows where {cols.ANNOTATION_TYPE} is frame_label into frame_range_label rows.'

    def ProcessStep(self, data: pandas.DataFrame) -> pandas.DataFrame:

        is_frame_label = (data[cols.ANNOTATION_TYPE] == 'frame_label')

        data.loc[is_frame_label, cols.FRAME_RANGE] = [ f'[{int(x)}, {int(x)}]' for x in data.loc[is_frame_label, cols.FRAME_INDEX] ]
        data.loc[is_frame_label, cols.FRAME_INDEX] = pandas.NA
        data.loc[is_frame_label, cols.ANNOTATION_TYPE] = 'frame_range_label'

        return data

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__)






