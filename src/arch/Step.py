import pandas
from arch import Base

class Step(Base):

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        self._raise_not_implemented(self.process)
