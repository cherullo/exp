import pandas
import numpy as np
from arch import Hasher, Step

class LastCount(Step):
    """ Keeps a set number of the last rows of the dataset.

    Args:
        Step (_type_): This is a preprocessing step.
    """
    def __init__(self, count: int):
        """
        Builds a preprocessing step which keeps the last count rows.

        Args:
            count (int): Number of rows to keep.
        """
        self.count = int(np.abs(count))

    def __str__(self) -> str:
        return f'LastCount({self.count})'

    def description(self) -> str:
        return f'Selects the last {self.count} rows.'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:

        if len(data) == 0:
            return data

        total_rows = len(data.index)
        count_to_return = int(np.min([self.count, total_rows]))

        if count_to_return is not self.count:
            print (f"{self.__class__.__name__}: kept less rows than asked for ({count_to_return} < {self.count})")

        return data[-count_to_return:]


    def add_hash(self, h: Hasher):
        h.ordered(self.__class__.__name__, self.count)
