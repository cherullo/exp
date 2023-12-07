import pandas

from exp.arch import Hasher, BaseStep

class Shuffle(BaseStep):
    """ Shuffles the dataset.

    Args:
        Step (_type_): This is a preprocessing step.
    """
    def __init__(self, seed: int):
        """
        Builds a preprocessing step which shuffles the dataset.

        Args:
            seed (int): Random seed.
        """
        self.seed = seed

    def __str__(self) -> str:
        return f'Shuffle({self.seed})'

    def description(self) -> str:
        return f'Shuffles the rows using seed = {self.seed}.'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        return data.sample(frac=1, random_state=self.seed)

    def add_hash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.seed)
