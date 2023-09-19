import importlib
import common.gtm_log as log
from common.consts import datasource_sdk
import common.consts.modules_and_index as module_name
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
                raise AttributeError("Attribute {} in module {} is not callable".format(sdkMethod, sdkName), module_name.MODULE_UTIL_DOWNLOADER_SDK, "downloader_method_executable_check")
        except ImportError:
            log.logError("module: {}".format(sdkName), module_name.MODULE_UTIL_DOWNLOADER_SDK, "cannot_import_module_by_name")
        except AttributeError:
            log.logError("module {} does not exists {}".format(sdkName, sdkMethod), module_name.MODULE_UTIL_DOWNLOADER_SDK, "encounter_attribute_err")

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
                    "cannot login||err_msg:{}||err_code:{}".format(loginRes.error_msg, loginRes.error_code), module_name.MODULE_UTIL_DOWNLOADER_SDK, "baostock_login_failed")
            log.logInfo("login success", module_name.MODULE_UTIL_DOWNLOADER_SDK, "baostock_login", module_name.MODULE_UTIL_DOWNLOADER_SDK, "baostock_login")
        except ImportError:
            log.logError("import_err", module_name.MODULE_UTIL_DOWNLOADER_SDK, "baostock_login")
        except AttributeError:
            log.logError("attribute_err", module_name.MODULE_UTIL_DOWNLOADER_SDK, "baostock_login")

    def BaostockLogout(self, sdkName, result):
        try:
            module = importlib.import_module(sdkName)
            logoutFunc = getattr(module, "logout")
            logoutRes = logoutFunc()
            if logoutRes.error_msg != "success":
                log.logError(
                    "err_msg:{}||err_code:{}".format(logoutRes.error_msg, logoutRes.error_code), module_name.MODULE_UTIL_DOWNLOADER_SDK, "baostock_logout_failed")
            log.logInfo("baostock logout success", module_name.MODULE_UTIL_DOWNLOADER_SDK, "baostock_logout")
        except ImportError:
            log.logError("import_err".format(sdkName), module_name.MODULE_UTIL_DOWNLOADER_SDK, "baostock_logout")
        except AttributeError:
            log.logError("attribute_err".format(sdkName), module_name.MODULE_UTIL_DOWNLOADER_SDK, "baostock_logout")

        data_list = []
        while (result.error_code == '0') & result.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(result.get_row_data())
        return pd.DataFrame(data_list, columns=result.fields)