from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log
import pandas_ta as ta
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1hour"

    def run(self, data):
        d = data["ohlcv"]
        h = data["holdings"]
        allocation_dict = {} 
        for i in self.tickers:
            rsi = RSI(i, d, 14)

            if rsi[-1] >= 50 and rsi[-2] < 50:
                allocation_dict = {i: 1}

            if rsi[-1] < 50:
                allocation_dict = {i: 0}

        return TargetAllocation(allocation_dict)