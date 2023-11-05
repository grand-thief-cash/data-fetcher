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