import unittest
import sdk_downloader
class TestSDKDownloader(unittest.TestCase):

    def test_download(self):
        module_name = 'akshare'
        method_name = 'stock_sse_summary'
        downloader = sdk_downloader.SDKDownloader()
        method = downloader.getMethodObj(module_name, method_name)

        result = downloader.invoke(module_name, method_name)
        # print(result['股票'])
        print(result)



if __name__ == '__main__':
    unittest.main()