import pandas
import annotations.columns as cols
from helpers import Hasher
from .BaseFilter import BaseFilter

class ChangeSeverity(BaseFilter):

    def __init__(self, original:str, replacement:str):
        self.original = original
        self.replacement = replacement

    def ToString(self) -> str:
        return f'ChangeSeverity[{self.original} -> {self.replacement}]'

    def Description(self) -> str:
        return f'Changes the {cols.SEVERITY} of rows from {self.original} to {self.replacement}'

    def ProcessStep(self, data: pandas.DataFrame) -> pandas.DataFrame:
        data.loc[data[cols.SEVERITY] == self.original, cols.SEVERITY] = self.replacement
        return data

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.original, self.replacement)
