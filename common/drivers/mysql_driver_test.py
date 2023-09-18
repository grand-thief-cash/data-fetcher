import unittest
import common.mysql_init as mysql_init
import mysql_driver as driver


class TestMysqlDriver(unittest.TestCase):

    def test_check_table_exists(self):
        mysql_init.init_connection("../../config/mysql_config.yml")
        isExisted = driver.check_table_exists("zhangsan")
        self.assertFalse(isExisted)
        print("done")

    def test_get_table_metadata(self):
        mysql_init.init_connection("../../config/mysql_config.yml")
        conn = mysql_init.get_connection()
        result = driver.get_table_metadata(conn, "akshare_stock_info_a_code_name")
        print(result)
