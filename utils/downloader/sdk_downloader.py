import importlib
import common.gma_log as log


class SDKDownloader:

    def getMethodObj(self, sdkName, sdkMethod, *args, **kwargs):
        try:
            module = importlib.import_module(sdkName)
            method = getattr(module, sdkMethod)
            if callable(method):  # 检查方法对象是否可调用
                # invoke example: method = get_method("akshare", "stock_sse_summary", param1, param2, key1=value1, key2=value2)
                return method
            else:
                raise AttributeError(f"Attribute '{sdkMethod}' in module '{sdkName}' is not callable")
        except ImportError:
            log.logError("cannot import modeule: {%s}" % sdkName)
        except AttributeError:
            log.logError("module '{%s}' does not exists '{%s}'"%(sdkName, sdkMethod))
            # print(f"module '{sdkName}' does not exists '{sdkMethod}'")

    def invoke(self, sdkName, sdkMethod, *args, **kwargs):
        method = self.getMethodObj(sdkName, sdkMethod)
        return method(*args, **kwargs)
