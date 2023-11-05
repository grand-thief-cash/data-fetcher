import pandas as pd


def calculate_pre_close(stock_csv, dividend_csv) -> pd.DataFrame:
    # 读取历史股票数据
    df_stock = pd.read_csv(stock_csv)
    print(df_stock)

    df_stock['date'] = pd.to_datetime(df_stock['date'])
    df_stock = df_stock.sort_values('date')

    # 读取分红，拆股，送股，派息等数据
    df_dividend = pd.read_csv(dividend_csv)
    print(df_dividend)

    df_dividend['date'] = pd.to_datetime(df_dividend['date'])
    df_dividend = df_dividend.sort_values('date')

    # 合并两个数据集
    df = pd.merge(df_stock, df_dividend, how='left', on='date')
    print(df)

    # 填充缺失值
    df[['bonus', 'split', 'dividend', 'ex-dividend']] = df[['bonus', 'split', 'dividend', 'ex-dividend']].fillna(0)
    print(df)

    # calculate pre_close price
    df['pre_close'] = df['close'].shift(1)
    df.loc[df['bonus'] != 0, 'pre_close'] = df['pre_close'] * (1 + df['bonus'])
    df.loc[df['split'] != 0, 'pre_close'] = df['pre_close'] / df['split']
    df.loc[df['dividend'] != 0, 'pre_close'] = df['pre_close'] - df['dividend']
    df.loc[df['ex-dividend'] != 0, 'pre_close'] = df['pre_close'] - df['ex-dividend']

    # fill the first raw of pre_close
    df['pre_close'].fillna(df['close'], inplace=True)
    return df


def cal_recover_price(df: pd.DataFrame):
    # 计算涨跌幅
    df['price_change'] = df['close'] / df['pre_close'] - 1
    # 计算复权因子
    df['adjust_factor'] = (1 + df['price_change']).cumprod()

    # 计算后复权价格
    df['back_adjust'] = df['adjust_factor'] * (
            df.iloc[0]['close'] / df.iloc[0]['adjust_factor'])

    return df


result = calculate_pre_close('price.csv', 'bonus_info.csv')
pd.set_option('display.max_columns', None)

print(result)
