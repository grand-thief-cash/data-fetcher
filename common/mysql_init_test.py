
import unittest

import common.mysql_init as mysql_init


class TestMysqlInit(unittest.TestCase):
    def test_init(self):
        config_path = "../config/mysql_config.yml"
        mysql_init.init_connection(config_path)
        conn = mysql_init.get_connection()
        self.assertIsNotNone(conn)


