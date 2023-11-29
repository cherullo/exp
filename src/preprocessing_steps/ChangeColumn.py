import pandas
from arch import Hasher, Step

class ChangeColumn(Step):
    """ 
    For each row, sets column to a new value if it has a certain value.

    Args:
        Step (_type_): This is a preprocessing step.
    """

    def __init__(self, column: str, originalValue: str, newValue: str):
        """ 
        Builds a preprocessing step that replaces originalValue with newValue in column.

        Args:
            column (str): Name of the column to process.
            originalValue (str): Value to search for.
            newValue (str): The replacement value.
        """
        self.column = column
        self.original = originalValue
        self.replacement = newValue

    def __str__(self) -> str:
        return f'ChangeColumn({self.column}, {self.original}, {self.replacement})'

    def description(self) -> str:
        return f'In row "{self.column}", change "{self.original}" to "{self.replacement}"'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        data.loc[data[self.column] == self.original, self.column] = self.replacement
        return data

    def add_hash(self, hasher: Hasher):
        hasher.ordered(self.__class__.__name__, self.original, self.replacement)
