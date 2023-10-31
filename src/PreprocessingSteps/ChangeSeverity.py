import pandas
import annotations.columns as cols
from helpers import Hasher
from ..arch.Step import Step

class ChangeSeverity(Step):

    def __init__(self, original:str, replacement:str):
        self.original = original
        self.replacement = replacement

    def ToString(self) -> str:
        return f'ChangeSeverity[{self.original} -> {self.replacement}]'

    def description(self) -> str:
        return f'Changes the {cols.SEVERITY} of rows from {self.original} to {self.replacement}'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        data.loc[data[cols.SEVERITY] == self.original, cols.SEVERITY] = self.replacement
        return data

    def add_hash(self, hasher: Hasher):
        hasher.ordered(self.__class__.__name__, self.original, self.replacement)
