import unittest

import akshare
import baostock as bs
import pandas as pd

import sdk_downloader


class TestSDKDownloader(unittest.TestCase):

    def test_download(self):
        module_name = 'akshare'
        method_name = 'stock_sse_summary'
        downloader = sdk_downloader.SDKDownloader()
        method = downloader.get_method_obj(module_name, method_name)

        result = downloader.invoke(module_name, method_name)
        # print(result['股票'])
        print(result)

    def test_download2(self):
        module_name = 'akshare'
        method_name = 'stock_zh_a_hist'
        downloader = sdk_downloader.SDKDownloader()
        method = downloader.get_method_obj(module_name, method_name)

        result = downloader.invoke(module_name, method_name, symbol="000001", period="daily", start_date="19900301",
                                   end_date='19950325', adjust="")
        print(result)
        result.to_csv('data1.csv', index=False, encoding='utf8')

    def test_download3(self):
        module_name = 'akshare'
        method_name = 'stock_fhps_detail_ths'
        downloader = sdk_downloader.SDKDownloader()
        method = downloader.get_method_obj(module_name, method_name)

        result = downloader.invoke(module_name, method_name, symbol="000001")
        print(result)
        result.to_csv('data2.csv', index=False, encoding='utf8')

    def test_download3(self):
        module_name = 'akshare'
        method_name = 'news_trade_notify_dividend_baidu'
        downloader = sdk_downloader.SDKDownloader()
        method = downloader.get_method_obj(module_name, method_name)

        result = downloader.invoke(module_name, method_name, date="20150413")
        print(result)
        result.to_csv('data3.csv', index=False, encoding='utf8')

    def test_download4(self):
        module_name = 'akshare'
        method_name = 'stock_zh_a_hist'
        downloader = sdk_downloader.SDKDownloader()
        method = downloader.get_method_obj(module_name, method_name)

        result = downloader.invoke(module_name, method_name, symbol="000001", period="daily", start_date="19900301",
                                   end_date='19950325', adjust="hfq")
        print(result)
        result.to_csv('data4.csv', index=False, encoding='utf8')

    def test_download5(self):
        module_name = 'akshare'
        method_name = 'stock_zh_a_daily'
        downloader = sdk_downloader.SDKDownloader()

        result = downloader.invoke(module_name, method_name, symbol="sz000001", start_date="19901103", end_date="19931103", adjust="hfq-factor")
        print(result)
        result.to_csv('data5.csv', index=False, encoding='utf8')

        # stock_zh_a_daily_qfq_df = akshare.stock_zh_a_daily(symbol="sz000001", start_date="19901103", end_date="19931103", adjust="hfq")
        # print(stock_zh_a_daily_qfq_df)

    def test_download6(self):
        module_name = 'akshare'
        method_name = 'stock_zh_b_daily'
        downloader = sdk_downloader.SDKDownloader()

        result = downloader.invoke(module_name, method_name, symbol="sz000001", start_date="1991-04-03", end_date="1992-04-03", adjust="hfq-factor")
        print(result)
        result.to_csv('data6.csv', index=False, encoding='utf8')

    def test_download7(self):
        module_name = 'baostock'
        method_name = 'query_adjust_factor'
        downloader = sdk_downloader.SDKDownloader()

        # 登陆系统
        lg = bs.login()
        # 显示登陆返回信息
        print('login respond error_code:' + lg.error_code)
        print('login respond  error_msg:' + lg.error_msg)

        # 查询2015至2017年复权因子
        rs_list = []
        rs_factor = bs.query_adjust_factor(code="sz.000001", start_date="1990-01-01", end_date="1992-04-03")
        while (rs_factor.error_code == '0') & rs_factor.next():
            rs_list.append(rs_factor.get_row_data())
        result_factor = pd.DataFrame(rs_list, columns=rs_factor.fields)
        # 打印输出
        print(result_factor)

        # 结果集输出到csv文件
        result_factor.to_csv("adjust_factor_data.csv", encoding="gbk", index=False)

        # 登出系统
        bs.logout()

    def test_download8(self):
        module_name = 'akshare'
        method_name = 'stock_fhps_detail_em'
        downloader = sdk_downloader.SDKDownloader()

        result = downloader.invoke(module_name, method_name, symbol="000001")
        print(result)
        result.to_csv('fenhong.csv', index=False, encoding='utf8')

        # stock_dividents_cninfo_df = akshare.stock_dividents_cninfo(symbol="600009")
        # print(stock_dividents_cninfo_df)

if __name__ == '__main__':
    unittest.main()
