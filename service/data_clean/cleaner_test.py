import copy
import unittest

from pandas import DataFrame
from pandas.core.arrays.floating import Float64Dtype
from pandas.core.arrays.string_ import StringDtype

from service.data_clean.cleaner import DataCleaner

CODE = '000001'


class TestCleaner(unittest.TestCase):

    def testExtendColumns(self):
        extend_columns = {
            "code": CODE,
            "adjust": None
        }
        cleaner = DataCleaner(MockDataProvider().get_df_today())
        cleaner.extend_columns(extend_columns)

        assert "code" in cleaner.df
        assert cleaner.df["code"][0] == CODE
        assert "adjust" in cleaner.df
        assert cleaner.df["adjust"][0] is None

    def testCheckDrift(self):
        provider = MockDataProvider()
        cleaner = DataCleaner(provider.get_df_today_with_modification())
        new, updated, removed = cleaner.check_drift(provider.get_df_yesterday(), ['code', 'date'])
        assert len(new) == 1 and new['date'].values[0] == '2023-06-06'
        assert len(updated) == 2 and '2023-06-04' in updated['date'].values
        assert len(removed) == 1 and removed['date'].values[0] == '2023-06-02'

    def testCheckDriftFirstTime(self):
        df = MockDataProvider().get_df_yesterday()
        cleaner = DataCleaner(df)
        new, updated, removed = cleaner.check_drift(None, ['code', 'date'])
        assert len(updated) == 0
        assert len(removed) == 0
        assert len(new) == len(df)

    def testFixDataType(self):
        cleaner = DataCleaner(MockDataProvider().get_df_today())
        cleaner.fix_data_type()

        assert isinstance(cleaner.df['date'].dtype, StringDtype)
        assert isinstance(cleaner.df['open'].dtype, Float64Dtype)
        assert isinstance(cleaner.df['desc'].dtype, StringDtype)


class MockDataProvider:
    data = [
        {'date': '2023-06-06', 'open': 12.00, 'close': 11.00, 'desc': 'desc6.......'},
        {'date': '2023-06-05', 'open': 13.00, 'close': 12.00, 'desc': 'desc5........................'},
        {'date': '2023-06-04', 'open': 14.00, 'close': 13.00, 'desc': 'desc4'},
        {'date': '2023-06-03', 'open': 15.00, 'close': 14.00, 'desc': 'desc3..........'},
        {'date': '2023-06-02', 'open': 10.00, 'close': 15.00, 'desc': 'desc2...'},
    ]

    def get_df_yesterday(self):
        df = DataFrame(self.data[1:])
        df['code'] = [CODE]*len(df)
        return df

    def get_df_today_with_modification(self):
        modified = copy.deepcopy(self.data[:-1])
        modified[1]['open'] = 10000
        modified[2]['close'] = 20000
        df = DataFrame(modified)
        df['code'] = [CODE]*len(df)
        return df

    def get_df_today(self):
        return DataFrame(self.data)
