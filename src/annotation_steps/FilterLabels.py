import pandas
from typing import List
import annotations.columns as cols
from helpers import Hasher
from .BaseFilter import BaseFilter

class FilterLabels(BaseFilter):

    def __init__(self, labels:List[str]):
        self.labels = [s for s in labels if (s)]

    def ToString(self) -> str:
        temp = ', '.join(self.labels)
        return f'FilterLabels[{temp}]'

    def Description(self) -> str:
        temp = ', '.join(self.labels)
        return f'Keeps all rows where the field \'{cols.LABEL}\' is in the following list: [{temp}]'

    def ProcessStep(self, data: pandas.DataFrame) -> pandas.DataFrame:
        return data[ data[cols.LABEL].isin( self.labels ) ]

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__).ordered(*self.labels)


