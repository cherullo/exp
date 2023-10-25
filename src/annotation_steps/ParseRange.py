import ast
import pandas
import numpy as np
import annotations.columns as cols
from helpers import Hasher
from .BaseFilter import BaseFilter

def parse_frameRange(x):
    ret = ast.literal_eval(x)
    ret = [ int(ret[0]), int(ret[1]) ] 

    if ret[0] < 0 or ret[1] < 0:
        raise Exception('Negative frame range.')

    return ret

class ParseRange(BaseFilter):

    def __init__(self):
        pass

    def ToString(self) -> str:
        return 'ParseRange'

    def Description(self) -> str:
        return f'Parses the {cols.FRAME_RANGE} column into a list of values.'

    def ProcessStep(self, data: pandas.DataFrame) -> pandas.DataFrame:

        is_frame_range_label = (data[cols.ANNOTATION_TYPE] == 'frame_range_label')
        has_frame_range = pandas.notna(data[cols.FRAME_RANGE])

        range_rows = is_frame_range_label & has_frame_range
        data.loc[range_rows, cols.FRAME_RANGE] = data.loc[range_rows, cols.FRAME_RANGE].apply(parse_frameRange, convert_dtype=False)

        return data

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__)
