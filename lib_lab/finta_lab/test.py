import os
import pandas as pd

from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from finta import TA

# Using same data set as unittests
data_file = os.path.join("btc-usdt.csv")

ohlc = pd.read_csv(data_file, index_col="date", parse_dates=True)

# Backtest.py wants column names as following:

# ohlc.columns = ["Close", "High", "Low", "Open", "Volume"]

# While finta wants it all in lowercase
# Simplest solution is to copy the columns

ohlc["Low"] = ohlc["low"]
ohlc["High"] = ohlc["high"]
ohlc["Open"] = ohlc["open"]
ohlc["Close"] = ohlc["close"]
ohlc["Volume"] = ohlc["volume"]


# Defining DEMA cross strategy
class DemaCross(Strategy):

    def init(self):

        self.ma1 = self.I(TA.DEMA, ohlc, 10)
        self.ma2 = self.I(TA.DEMA, ohlc, 20)



    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()

bt = Backtest(ohlc, DemaCross, cash=1000000, commission=0.025)

bt.run()
