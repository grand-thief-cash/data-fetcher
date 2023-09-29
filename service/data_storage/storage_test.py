import unittest
from time import sleep

import sqlalchemy
from sqlalchemy import Engine, text

from common.mysql_init import init_connection, get_connection, get_engine
from service.data_clean.cleaner import DataCleaner
from service.data_clean.cleaner_test import MockDataProvider
from service.data_storage.storage import DataStorage


class TestStorage(unittest.TestCase):

    def testEngine(self):
        init_connection("../../config/mysql_config.yml")
        storage = DataStorage('test_table1', get_engine, {})
        assert type(storage._get_engine()) is Engine

    def testTableExists(self):
        init_connection("../../config/mysql_config.yml")

        print("test table not exists")
        conn = get_connection()
        conn.execute(text('DROP TABLE IF EXISTS test_table2;'))
        storage = DataStorage('test_table2', get_engine, {})
        assert storage.table_exists() is False

        print("test table exists")
        conn = get_connection()
        conn.exec_driver_sql('''
        create table if not exists quant_storage.test_table2
        (
            column_name int null
        );''')
        assert storage.table_exists() is True

        print("cleanup tables")
        conn = get_connection()
        conn.execute(text('DROP TABLE IF EXISTS test_table2;'))

    def testFirstTimeSave(self):
        table_name = 'test_mock_tb'

        init_connection("../../config/mysql_config.yml")
        conn = get_connection()
        conn.exec_driver_sql(f'DROP TABLE IF EXISTS {table_name};')

        df = MockDataProvider().get_df_today()
        df = df.convert_dtypes(True, True, False, True, True)
        storage = DataStorage(table_name, get_engine, {'date': sqlalchemy.VARCHAR(length=32)})
        storage.save(df, None, None, [])

        resp = conn.exec_driver_sql(f'DESCRIBE {table_name};')
        assert resp.first()[1] == 'varchar(32)'

        conn.exec_driver_sql(f'DROP TABLE IF EXISTS {table_name};')
        conn.close()

    def testGet(self):
        table_name = 'test_mock_tb'
        init_connection("../../config/mysql_config.yml")
        conn = get_connection()
        conn.exec_driver_sql(f'DROP TABLE IF EXISTS {table_name};')

        CODE = 'abcdefg'
        df = MockDataProvider().get_df_today()
        df['code'] = [CODE] * len(df)
        storage = DataStorage(table_name, get_engine, {})
        storage.save(df, None, None, [])
        sleep(1)

        _df = storage.get([f'code="{CODE}"', '1=1', '2=2'])
        assert len(df) == len(_df)

        conn.exec_driver_sql(f'DROP TABLE IF EXISTS {table_name};')
        conn.close()

    def testDay2Save(self):
        table_name = 'test_mock_tb'
        init_connection("../../config/mysql_config.yml")
        conn = get_connection()
        conn.exec_driver_sql(f'DROP TABLE IF EXISTS {table_name};')

        df1 = MockDataProvider().get_df_yesterday()
        storage = DataStorage(table_name, get_engine, {'date': sqlalchemy.VARCHAR(length=32)})
        storage.save(df1, None, None, [])

        df2 = MockDataProvider().get_df_today_with_modification()
        cleaner = DataCleaner(df2)
        new, updated, deleted = cleaner.check_drift(df1, ['code', 'date'])
        storage.save(new, updated, deleted, ['code', 'date'])

        df_in_db = storage.get([f'code="000001"'])
        assert len(df_in_db) == 5
