import pandas as pd

# 历史价格数据
data = {
    '日期': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05'],
    '价格': [100.0, 105.0, 110.0, 115.0, 120.0]
}

df = pd.DataFrame(data)

# 分红日期和比例
dividend_dates = ['2022-01-02', '2022-01-04']
dividend_ratios = [0.1, 0.2]  # 分红比例为10%和20%

# 按日期升序排序
df.sort_values('日期', ascending=True, inplace=True)

# 初始化复权因子
adjustment_factor = 1.0

# 初始化复权价格列
df['复权价格'] = df['价格']

# 遍历历史价格数据进行复权计算
for i in range(len(df)):
    if df.iloc[i]['日期'] in dividend_dates:
        # 分红日期，更新复权因子
        dividend_ratio = dividend_ratios[dividend_dates.index(df.iloc[i]['日期'])]
        adjustment_factor *= (1 + dividend_ratio)

    # 计算复权后的价格
    df.loc[df.index[i], '复权价格'] = df.iloc[i]['价格'] / adjustment_factor

# 按日期升序排序
df.sort_values('日期', ascending=True, inplace=True)

# 打印复权后的价格数据
print(df[['日期', '复权价格']])
