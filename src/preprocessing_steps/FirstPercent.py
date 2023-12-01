import pandas
from arch import Hasher, Step

class FirstPercent(Step):
    """ Keeps a set number of the first rows of the dataset, defined as a percentage of the total number of rows.

    Args:
        Step (_type_): This is a preprocessing step.
    """
    def __init__(self, percent: float):
        """
        Builds a preprocessing step which keeps the top rows as a percentage of the total number of rows.

        Args:
            count (float): Percentage of rows to keep.
        """

        if percent < 0.0 or percent > 1.0:
            raise Exception(f'Invalid percentage in {self.__class__.__name__}: {percent}')

        self.percent = percent

    def __str__(self) -> str:
        return f'FirstPercent({self.percent})'

    def description(self) -> str:
        return f'Selects the first {self.percent * 100.0}% of images.'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        if len(data) == 0:
            return data

        total_rows = len(data.index)

        count_to_return = int(self.percent * total_rows)

        return data[0:count_to_return]

    def add_hash(self, h: Hasher):
        h.ordered(self.__class__.__name__, self.percent)
