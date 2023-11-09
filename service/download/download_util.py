

class DownloadUtil:
    def mysql_tablename_generation(self, sdk_name: str, func_name:str, params: dict):
        # 提取params字典中的所有值并按字母排序
        sorted_values = sorted(params.values())

        # 使用下划线拼接排序后的值
        sorted_params = '_'.join(sorted_values)

        # 拼接sdk_name、func_name和stage_name
        # result = f"{sdk_name}_{func_name}_{stage_name}"
        result = f"{sdk_name}_{func_name}_{sorted_params}"

        return result




sdk_name = "akshare"
func_name = "stock_szse_sector_summary"
params = {
    "symbol": "sh000300",
    "adjust": "hfq",
    "period": "cherry",
}

DownloadUtil = DownloadUtil()

result = DownloadUtil.mysql_tablename_generation(sdk_name, func_name, params)
print(result)
print(len(result))

