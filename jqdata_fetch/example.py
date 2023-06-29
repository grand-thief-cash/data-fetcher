import requests, json
import pandas as pd

#获取调用凭证
url = "https://dataapi.joinquant.com/apis"
body = {
    "method": "get_token",
    "mob": "",  #ID是申请JQData时所填写的手机号
    "pwd": "",  # Password为聚宽官网登录密码，新申请用户默认为手机号后6位
}
response = requests.post(url, data=json.dumps(body))
token = response.text

#调用get_all_securities函数获取所有股票信息
body = {
    "method": "get_all_securities",
    "token": token,
    "code": "stock",
    "date": "2019-01-15"
}
response = requests.post(url, data=json.dumps(body))
stock = response.text

#写入CSV文件
with open('C:/Users/jase8/Desktop/test/stock.csv', 'w')as f:
    f.write(stock)

#读取CSV文件转化成dataframe
df = pd.read_csv('C:/Users/jase8/Desktop/test/stock.csv',
'utf-8',engine='python')
print(df)