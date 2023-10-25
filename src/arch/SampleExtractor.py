import ast
import pandas
import annotations.columns as cols
import os
import arch.dataset_columns as dataset_columns


def _new_df(data=None) -> pandas.DataFrame:
    return pandas.DataFrame(data=data, columns=dataset_columns.all)


class SampleExtractor():
    def __init__(self, base_path: str):
        self.base_path = base_path

    def _process_row(self, row: pandas.Series) -> pandas.DataFrame:
        ret = []

        output = row[cols.SEVERITY]
        frame_range = row[cols.FRAME_RANGE]

        base_name = os.path.splitext(row[cols.DICOM_FILENAME])[0]
        temp_path = os.path.join(self.base_path, base_name)

        return [ [f'{temp_path}_{i}.png', None, output] for i in range(frame_range[0], frame_range[1] + 1)]

    def extract(self, df: pandas.DataFrame) -> pandas.DataFrame:

        new_rows = []

        for _, row in df.iterrows():
            new_rows.extend(self._process_row(row))

        return pandas.DataFrame(data=new_rows, columns=dataset_columns.all)
