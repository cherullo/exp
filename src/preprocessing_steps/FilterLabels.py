import pandas
from typing import List
import annotations.columns as cols
from arch import Hasher, Step

class FilterLabels(Step):

    def __init__(self, labels: List[str]):
        self.labels = [s for s in labels if (s)]

    def ToString(self) -> str:
        temp = ', '.join(self.labels)
        return f'FilterLabels[{temp}]'

    def description(self) -> str:
        temp = ', '.join(self.labels)
        return f'Keeps all rows where the field \'{cols.LABEL}\' is in the following list: [{temp}]'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        return data[ data[cols.LABEL].isin( self.labels ) ]

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__).ordered(*self.labels)


