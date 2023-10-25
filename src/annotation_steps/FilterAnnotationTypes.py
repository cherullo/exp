import pandas
from typing import List
import annotations.columns as cols
from helpers import Hasher
from .BaseFilter import BaseFilter

class FilterAnnotationTypes(BaseFilter):
    def __init__(self, annotationTypes:List[str]):
        self.annotationTypes = [s for s in annotationTypes if (s)]

    def ToString(self) -> str:
        temp = ', '.join(self.annotationTypes)
        return f'FilterLabels[{temp}]'

    def Description(self) -> str:
        temp = ', '.join(self.annotationTypes)
        return f'Keeps all rows where the field \'{cols.ANNOTATION_TYPE}\' is in the following list: [{temp}]'

    def ProcessStep(self, data: pandas.DataFrame) -> pandas.DataFrame:
        return data[ data[cols.ANNOTATION_TYPE].isin( self.annotationTypes ) ]

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__).ordered(*self.annotationTypes)
