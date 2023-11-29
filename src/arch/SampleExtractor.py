import pandas
import os
import arch.dataset_columns as dataset_columns

# def _new_df(data=None) -> pandas.DataFrame:
#     return pandas.DataFrame(data=data, columns=dataset_columns.all)

class SampleExtractor():
    def __init__(self, base_path: str, label_column: str, image_column: str):
        self.base_path = base_path
        self.label_column = label_column
        self.image_column = image_column

    def _process_row(self, row: pandas.Series) -> pandas.DataFrame:
        base_name = row[self.image_column]
        temp_path = os.path.join(self.base_path, base_name)

        label = row[self.label_column]

        return [ [f'{temp_path}', None, label] ]

    def extract(self, df: pandas.DataFrame) -> pandas.DataFrame:

        new_rows = []

        for _, row in df.iterrows():
            new_rows.extend(self._process_row(row))

        return pandas.DataFrame(data=new_rows, columns=dataset_columns.all)
