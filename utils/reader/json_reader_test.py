import unittest

from utils.reader.json_reader import read_json_file


class TestJsonReader(unittest.TestCase):

    def test_json_reader(self):
        json_file_path = '../../service/data_fetch/fetch_akshare/stock_data/task/single_time_task.json'
        json_string = read_json_file(json_file_path)
        print(json_string)
