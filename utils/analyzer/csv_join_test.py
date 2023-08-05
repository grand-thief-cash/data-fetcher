import unittest

from utils.analyzer.csv_join import merge_two_csv_by_index


class TestMergeCSV(unittest.TestCase):

    def test_merge_two_csv_by_index(self):
        # 替换以下参数为你实际的文件路径和索引列
        csv1_path = "../downloader/data1.csv"
        csv2_path = "../downloader/data4.csv"
        index_col = "日期"  # 指定用于连接的索引列的名称
        output_csv = "output_merged_csv.csv"

        # 调用函数
        merge_two_csv_by_index(csv1_path, csv2_path, index_col, output_csv)

