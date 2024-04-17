from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log
import pandas_ta as ta
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SOXX"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "4hour"

    def run(self, data):
        d = data["ohlcv"]
        h = data["holdings"]
        allocation_dict = {} 
        for i in self.tickers:
            pclose = d[-1][i]['close']
            popen = d[-1][i]['open']
            mfi   = MFI(i, d, 5)
            sma   = SMA(i, d, 20)

            if (pclose > sma[-1]) and \
               (mfi[-1] > 40 and mfi[-2] <= 40):
                allocation_dict = {i: 1}

            if (pclose < sma[-1]) and (mfi[-1] < 60):
                allocation_dict = {i: 0}
            
            # # MFI is overbought, sell
            if mfi[-1] >= 85:
                allocation_dict = {i: 0}


        return TargetAllocation(allocation_dict)