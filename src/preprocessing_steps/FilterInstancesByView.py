import pandas
from typing import List
import annotations.columns as cols
from arch import Hasher, Step

class FilterInstancesByView(Step):
    def __init__(self, view:str):
        self.view = view

    def ToString(self) -> str:
        return f'FilterInstancesByView[{self.view}]'

    def Description(self) -> str:
        return f'Keeps all rows whose instanceUID is in the {self.view}.'

    def process(self, data: pandas.DataFrame) -> pandas.DataFrame:

        temp = data.loc[(data[cols.SEVERITY] == self.view) & (data[cols.ANNOTATION_TYPE] == 'instance_label')]

        instanceUIDs = temp[cols.INSTANCE_UID].tolist()

        print(instanceUIDs)

        return data[ data[cols.INSTANCE_UID].isin( instanceUIDs ) ].copy(deep=True)

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__, self.view)

