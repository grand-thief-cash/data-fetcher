from typing import Dict
import datacompy
from pandas import DataFrame, Series


class DataCleaner:
    df: DataFrame

    def __init__(self, df: DataFrame):
        self.df = DataFrame(df, copy=True)

    def extend_columns(self, extend_columns: Dict):
        count = len(self.df)
        for k, v in extend_columns.items():
            self.df[k] = Series([v] * count)

    def fix_data_type(self):
        if not self.fix_data_type:
            return

        self.df = self.df.convert_dtypes(
            infer_objects=True, convert_string=True, convert_integer=False, convert_floating=True, convert_boolean=True
        )

    def check_drift(self, previous_df: DataFrame | None, key_columns: list[str]) -> (DataFrame, DataFrame, DataFrame):
        """
        Compare df to previous_df
        :rtype: new in df, updated in df, removed in df
        """
        if not key_columns:
            raise Exception('should provide at least 1 key_columns')

        if previous_df is None:
            previous_df = DataFrame(self.df.head(0))
        for key in key_columns:
            if key not in self.df:
                raise Exception(f'key {key} is not in self.df')
            if len(previous_df) > 0 and key not in previous_df:
                raise Exception(f'key {key} is not in previous_df')

        comp = datacompy.Compare(self.df, previous_df, join_columns=['code', 'date'])
        return comp.df1_unq_rows, comp.all_mismatch(), comp.df2_unq_rows
