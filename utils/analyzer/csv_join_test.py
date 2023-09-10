import unittest

from utils.analyzer.csv_join import merge_two_csv_by_index, merge_two_csv_by_two_index


class TestMergeCSV(unittest.TestCase):

    def test_merge_two_csv_by_index(self):
        # 替换以下参数为你实际的文件路径和索引列
        csv1_path = "../downloader/data1.csv"
        csv2_path = "../downloader/data4.csv"
        index_col = "日期"  # 指定用于连接的索引列的名称
        output_csv = "output_merged_csv.csv"

        # 调用函数
        merge_two_csv_by_index(csv1_path, csv2_path, index_col, output_csv)




    def test_merge_two_csv_by_two_index(self):
        # 替换以下参数为你实际的文件路径和索引列
        csv1_path = "../downloader/pingan_back_adjust_dongcai.csv"
        csv2_path = "../downloader/pingan_back_adjust_sina.csv"
        index_col1 = "日期"  # 指定用于连接的索引列的名称
        index_col2 = "date"  # 指定用于连接的索引列的名称
        output_csv = "pingan_back_adjust_dongcai_sina.csv"

        # 调用函数
        merge_two_csv_by_two_index(csv1_path, csv2_path, index_col1, index_col2, output_csv)

    def test_merge_two_csv_by_two_index2(self):
        # 替换以下参数为你实际的文件路径和索引列
        csv1_path = "pingan_back_adjust_dongcai_sina.csv"
        csv2_path = "../downloader/pingan_back_adjust_baostock.csv"
        index_col1 = "日期"  # 指定用于连接的索引列的名称
        index_col2 = "date"  # 指定用于连接的索引列的名称
        output_csv = "pingan_back_adjust_dongcai_sina2.csv"

        # 调用函数
        merge_two_csv_by_two_index(csv1_path, csv2_path, index_col1, index_col2, output_csv)

