from typing import List

import pandas

from arch import Hasher, BaseStep

class FilterColumn(BaseStep):
    """
    Keeps all rows where the value of certaing column is in a given list.

    Args:
        Step (_type_): This is a preprocessing step.
    """

    def __init__(self, column: str, values: List[str]):
        """
        Builds a preprocessing step that keeps all rows where column has a value in values.

        Args:
            column (str): Column to filter.
            values (List[str]): List of values.
        """
        self.column = column
        self.values = [s for s in values if (s)]

    def __str__(self) -> str:
        temp = ', '.join([f'"{x}"' for x in self.values])
        return f'FilterColumn("{self.column}", [{temp}])'

    def description(self) -> str:
        temp = ', '.join([f'"{x}"' for x in self.values])
        return f'Keeps all rows where the column "{self.column}" has any of the following values: {temp}'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        return data[ data[self.column].isin(self.values) ]

    def add_hash(self, hasher:Hasher):
        hasher.ordered(self.__class__.__name__, self.column).unordered(*self.values)


