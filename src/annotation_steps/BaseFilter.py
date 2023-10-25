import pandas
from arch import Base
from helpers import Hasher

class BaseFilter(Base):

    def ProcessStep(self, data: pandas.DataFrame) -> pandas.DataFrame:
        _raise_not_implemented(ProcessStep)
