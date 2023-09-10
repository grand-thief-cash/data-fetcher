import unittest

import akshare
import baostock as bs
import pandas as pd

import sdk_downloader


class TestSDKDownloader(unittest.TestCase):



    def test_download_pingan(self):
        #东财 历史行情数据
        #平安银行，未经复权数据
        module_name = 'akshare'
        method_name = 'stock_zh_a_hist'
        downloader = sdk_downloader.SDKDownloader()
        method = downloader.getMethodObj(module_name, method_name)

        result = downloader.invoke(module_name, method_name, symbol="000001", period="daily", start_date="19910403", adjust="")
        print(result)
        result.to_csv('pingan_non_adjust_dongcai.csv', index=False, encoding='utf8')

    def test_download_pingan2(self):
        #东财 历史行情数据
        #平安银行，后复权数据
        module_name = 'akshare'
        method_name = 'stock_zh_a_hist'
        downloader = sdk_downloader.SDKDownloader()
        method = downloader.getMethodObj(module_name, method_name)

        result = downloader.invoke(module_name, method_name, symbol="000001", period="daily", start_date="19910403", adjust="hfq")
        print(result)
        result.to_csv('pingan_back_adjust_dongcai.csv', index=False, encoding='utf8')


    def test_download_pingan3(self):
        #新浪 历史行情数据
        #平安银行，未复权数据
        module_name = 'akshare'
        method_name = 'stock_zh_a_daily'
        downloader = sdk_downloader.SDKDownloader()
        method = downloader.getMethodObj(module_name, method_name)

        result = downloader.invoke(module_name, method_name, symbol="sz000001", start_date="19910403")
        print(result)
        result.to_csv('pingan_non_adjust_sina.csv', index=False, encoding='utf8')

    def test_download_pingan4(self):
        #新浪 历史行情数据
        #平安银行，后复权数据
        module_name = 'akshare'
        method_name = 'stock_zh_a_daily'
        downloader = sdk_downloader.SDKDownloader()
        method = downloader.getMethodObj(module_name, method_name)

        result = downloader.invoke(module_name, method_name, symbol="sz000001", start_date="19910403", adjust="hfq")
        print(result)
        result.to_csv('pingan_back_adjust_sina.csv', index=False, encoding='utf8')


    def test_download_pingan5(self):
        #新浪 历史行情数据
        #平安银行，后复权因子
        module_name = 'akshare'
        method_name = 'stock_zh_a_daily'
        downloader = sdk_downloader.SDKDownloader()
        method = downloader.getMethodObj(module_name, method_name)

        result = downloader.invoke(module_name, method_name, symbol="sz000001",  adjust="hfq-factor")
        print(result)
        result.to_csv('pingan_back_adjust_factor_sina.csv', index=False, encoding='utf8')

    def test_download_pingan6(self):
        #baoshock
        # 历史行情数据
        #平安银行，未复权数据
        #### 登陆系统 ####
        lg = bs.login()
        # 显示登陆返回信息
        print('login respond error_code:' + lg.error_code)
        print('login respond  error_msg:' + lg.error_msg)

        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus("sz.000001", "date,code,open,high,low,close", start_date='1991-04-03', frequency="d", adjustflag="3")
        print('query_history_k_data_plus respond error_code:' + rs.error_code)
        print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        #### 结果集输出到csv文件 ####
        result.to_csv('pingan_non_adjust_baostock.csv', index=False, encoding='utf8')
        print(result)

        #### 登出系统 ####
        bs.logout()


    def test_download_pingan7(self):
        #baoshock
        # 历史行情数据
        #平安银行，未复权数据
        #### 登陆系统 ####
        lg = bs.login()
        # 显示登陆返回信息
        print('login respond error_code:' + lg.error_code)
        print('login respond  error_msg:' + lg.error_msg)

        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus("sz.000001", "date,code,open,high,low,close", start_date='1991-04-03', frequency="d", adjustflag="1")
        print('query_history_k_data_plus respond error_code:' + rs.error_code)
        print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        #### 结果集输出到csv文件 ####
        result.to_csv('pingan_back_adjust_baostock.csv', index=False, encoding='utf8')
        print(result)

        #### 登出系统 ####
        bs.logout()


if __name__ == '__main__':
    unittest.main()
