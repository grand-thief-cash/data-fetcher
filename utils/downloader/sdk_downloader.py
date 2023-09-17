import importlib
import common.gtm_log as log
from common.consts import datasource_sdk
from utils.reflect_util.wrap import wrap_method_with_hooks
import pandas as pd

class SDKDownloader:

    def getMethodObj(self, sdkName, sdkMethod, *args, **kwargs):
        try:
            module = importlib.import_module(sdkName)
            method = getattr(module, sdkMethod)
            if callable(method):  # 检查方法对象是否可调用
                # invoke example: method = get_method("akshare", "stock_sse_summary", param1, param2, key1=value1, key2=value2)
                if sdkName == datasource_sdk.BAOSTOCK:
                    return self.wrap_baostock_method_with_hooks(method, self.BaostockLogin, self.BaostockLogout, sdkName)
                return method
            else:
                raise AttributeError("Attribute {} in module {} is not callable".format(sdkMethod, sdkName))
        except ImportError:
            log.logError("cannot import module: {}".format(sdkName))
        except AttributeError:
            log.logError("module {} does not exists {}".format(sdkName, sdkMethod))

    def invoke(self, sdkName, sdkMethod, *args, **kwargs):
        method = self.getMethodObj(sdkName, sdkMethod)
        return method(*args, **kwargs)



    #   Following are used in Baostock download
    def wrap_baostock_method_with_hooks(self, method, pre_hook, post_hook, sdkName, *args, **kwargs):
        def wrapped_method(*args, **kwargs):
            pre_hook(sdkName)  # 在调用method前执行前置钩子，并传递sdkName
            result = method(*args, **kwargs)
            newResult = post_hook(sdkName, result)  # 在调用method后执行后置钩子，并传递sdkName
            return newResult

        return wrapped_method

    def BaostockLogin(self, sdkName):
        try:
            module = importlib.import_module(sdkName)
            loginFunc = getattr(module, "login")
            loginRes = loginFunc()
            if loginRes.error_msg != "success":
                log.logError(
                    "cannot login baostock||err_msg:{}||err_code:{}".format(loginRes.error_msg, loginRes.error_code))
            log.logInfo("{} login success".format(sdkName))
        except ImportError:
            log.logError("cannot import module: {}".format(sdkName))
        except AttributeError:
            log.logError("Attribute 'login' in module {} is missing".format(sdkName))

    def BaostockLogout(self, sdkName, result):
        try:
            module = importlib.import_module(sdkName)
            logoutFunc = getattr(module, "logout")
            logoutRes = logoutFunc()
            if logoutRes.error_msg != "success":
                log.logError(
                    "cannot logout baostock||err_msg:{}||err_code:{}".format(logoutRes.error_msg, logoutRes.error_code))
            log.logInfo("{} logout success".format(sdkName))
        except ImportError:
            log.logError("cannot import module: {}".format(sdkName))
        except AttributeError:
            log.logError("Attribute 'logout' in module {} is missing".format(sdkName))

        data_list = []
        while (result.error_code == '0') & result.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(result.get_row_data())
        return pd.DataFrame(data_list, columns=result.fields)