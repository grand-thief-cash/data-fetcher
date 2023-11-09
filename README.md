# data-fetcher

## ENV Install

- Install python 11
- Activate virtual env: .\venv\Scripts\activate  
- install virtual env: pip install -r ./requirements/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


Clean current env:
```
pip freeze > requirements/remove.txt
pip uninstall -r requirements/remove.txt -y
```

## Development
### Data Source
- akshare: https://akshare.xyz/tutorial.html#id1
- Baostock: http://baostock.com/baostock/index.php/%E9%A6%96%E9%A1%B5
## Development Ref

### LOG
- loguru doc: https://blog.csdn.net/Kangyucheng/article/details/112794185
- loguru csdn: https://blog.csdn.net/Kangyucheng/article/details/112794185

### Unit test
- unittest: https://docs.python.org/zh-cn/3/library/unittest.html

### 文档
基于套利定价理论的七因子策略: https://mp.weixin.qq.com/s/HpRKPW6bGNTXoCXmZdK8ow

量化小学: https://www.bilibili.com/video/BV1xW411H7kE/?p=2&vd_source=7880edeb390f6ef3f8bdd4ce778050f3

如何搭建自己的股票高频数据库（Python）:https://zhuanlan.zhihu.com/p/488375029


### Requirements:
1. API data trunks
- 第一期只做静态数据拉取，不做periodically update
- 每一个api 参数不同时候，进行拆表，有需要再join
- table name 手动填写，根据value 排序
- task_*.json 只是作为task template 模板，具体的执行周期又任务系统来注入运行周期参数
- run_task 函数内部不关心具体的下载任务
- table name rules：
	1. API （join different params）
	2. step stage
2. data processing 
- 第一期，每一个processing 单数实现 不做工具化 
- table name rules：
	1. API （join different params）
	2. step stage
3. logging format
4. data checking akshare/tushare
5. checking back adjust


```json

{
    "task_name": "任务名称",  
    "concrete_task": {

		"fetch": {
			"module": "akshare",
			"method_name": "stock_info_sh_name_code",
			"input_param": {},
		},
		"clean": {
			"fields_mapping":{
				"证券代码": "security_id"
			},
			"transform_axis": true, // 是否需要行列转换
		},
        "store": {
            "table_name": "stock_info_a_code_name",
            "fields_data_type": {
                "security_id": "char(8)",
                "security_desc": "varchar(8)",
                "上市日期": "datetime"
            },
			"primary_key": ["security_id", "date"]
        }
    }
}

```