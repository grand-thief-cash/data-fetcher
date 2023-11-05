import pandas as pd

from finta import TA
import datetime

start = datetime.datetime.now()
ohlc = pd.read_csv("btc-usdt.csv", index_col="date", parse_dates=True)



ohlc.columns = ['close', 'volume', 'open', 'high', 'low']

# def split(dollar: str) -> float:
#     return float(dollar.split("$")[1])

#
# ohlc["close"] = ohlc["close"].apply(split)
#
# ohlc["low"] = ohlc["low"].apply(split)
#
# ohlc["high"] = ohlc["high"].apply(split)
#
# ohlc["open"] = ohlc["open"].apply(split)

tmp_result = TA.RSI(ohlc)



ten_rows = tmp_result.tail(10)

print(ten_rows)

end = datetime.datetime.now()

print(end-start)