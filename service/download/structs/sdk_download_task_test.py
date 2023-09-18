# -*- coding: utf-8 -*-
import json
import unittest

import common.mysql_init as mysql_init
from service.download.structs.sdk_download_task import object_decoder
from utils.reader.json_reader import read_json_file


class TestSDKDownloadTaskTest(unittest.TestCase):

    def test_download(self):
        json_file_path = '../../data_fetch/fetch_akshare/stock_data/task/single_time_task.json'
        json_string = read_json_file(json_file_path)

        task = json.loads(json_string, object_hook=object_decoder)
        print(task.task_name)
        self.assertEqual( task.task_name, "股票列表-上证")

