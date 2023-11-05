import os
import pandas as pd

from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from finta import TA

# Using same data set as unittests
data_file = os.path.join("btc-usdt.csv")

ohlc = pd.read_csv(data_file, index_col="date", parse_dates=True)

# Backtest.py wants column names as following:

ohlc.columns = ['close', 'high','low', 'open', 'volume']


result = TA.RSI(ohlc)

print(result.tail(10))