from typing import List

import pandas

from arch import Hasher, Step

class FilterColumn(Step):

    def __init__(self, column: str, values: List[str]):
        self.column = column
        self.values = [s for s in values if (s)]

    def __str__(self) -> str:
        temp = ', '.join(self.values)
        return f'FilterColumn["{self.column}" isin [{temp}]]'

    def description(self) -> str:
        temp = ', '.join(self.values)
        return f'Keeps all rows where the column \'{self.column}\' has any of the following values: [{temp}]'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        return data[ data[self.column].isin(self.values) ]

    def add_hash(self, hasher:Hasher):
        hasher.ordered(self.__class__.__name__, self.column).unordered(*self.values)


