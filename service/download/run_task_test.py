import unittest

from service.download import run_task, run_task_v2
import common.mysql_init as mysql_init


class TestRunTask(unittest.TestCase):

    def test_run_task(self):
        json_file_path = '../data_fetch/fetch_akshare/stock_data/task/single_time_task.json'
        mysql_config = '../../config/mysql_config.yml'

        mysql_init.init_connection(mysql_config)
        run_task.run_task(json_file_path)

    def test_run_task_v2(self):
        json_file_path = '../data_fetch/fetch_akshare/stock_data/task/single_time_task2.json'
        mysql_config = '../../config/mysql_config.yml'

        mysql_init.init_connection(mysql_config)
        run_task_v2.run_task_v2(json_file_path)