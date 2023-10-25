import pandas
from .. import Base

class BaseFilter(Base):

    def ProcessStep(self, data: pandas.DataFrame) -> pandas.DataFrame:
        _raise_not_implemented(ProcessStep)
