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
        return "1day"

    def run(self, data):
        d = data["ohlcv"]
        h = data["holdings"]
        allocation_dict = {} 
        for i in self.tickers:
            close = d[-1][i]['close']
            mfi  = MFI(i, d, 5)

            if mfi[-1] <= 20:
                allocation_dict = {i: 1}

            if mfi[-1] >= 80:
                allocation_dict = {i: 0}


        return TargetAllocation(allocation_dict)