import pandas
from typing import List
import annotations.columns as cols
from arch import Hasher, Step

class FilterSeverities(Step):

    def __init__(self, severities:List[str]):
        self.severities = [s for s in severities if (s)]

    def ToString(self) -> str:
        temp = ', '.join(self.severities)
        return f'FilterSeverities[{temp}]'

    def Description(self) -> str:
        temp = ', '.join(self.severities)
        return f'Keeps all rows where the field \'{cols.SEVERITY}\' is in the following list: [{temp}]'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        return data[ data[cols.SEVERITY].isin( self.severities ) ]

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__).unordered(*self.severities)





