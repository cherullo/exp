from abc import abstractmethod

import pandas

from arch import Base

class Step(Base):
    """ 
    A data preprocessing step. Creates a new DataFrame based on an existing one.
    Should not alter the original DataFrame in any way.

    Args:
        Base (_type_): This is a hashable type.
    """
    @abstractmethod
    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        pass
