from abc import abstractmethod

import pandas

from arch import Base

class BaseStep(Base):
    """ 
    A data preprocessing step. Creates a new DataFrame based on an existing one.
    Should not alter the original DataFrame in any way.

    Args:
        Base (_type_): This is a hashable type.
    """
    @abstractmethod
    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:
        """ Applies this preprocessing step in data and returns the results.

        Args:
            data (pandas.DataFrame): Data to process.

        Returns:
            pandas.DataFrame: Processed data.
        """
        pass
