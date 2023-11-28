import pandas

from arch import Hasher, Step

class Shuffle(Step):
    def __init__(self, seed):
        self.seed = seed

    def ToString(self) -> str:
        return f'Shuffle({self.seed})'

    def Description(self) -> str:
        return f'Shuffles the rows using seed = {self.seed}.'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        return data.sample(frac=1, random_state=self.seed)

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.seed)
