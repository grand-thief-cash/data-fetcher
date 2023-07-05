# data-fetcher

## Knowledge Base


## ENV Install

- Install python 11
- Activate virtual env: .\venv\Scripts\activate  
- install virtual env: pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


Clean current env:
```
pip freeze > requirements/remove.txt
pip uninstall -r requirements/remove.txt -y
```

## Development Ref

### LOG
- loguru doc: https://blog.csdn.net/Kangyucheng/article/details/112794185
- loguru csdn: https://blog.csdn.net/Kangyucheng/article/details/112794185

### Unit test
- unittest: https://docs.python.org/zh-cn/3/library/unittest.html