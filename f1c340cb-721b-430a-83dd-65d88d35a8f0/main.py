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
            
            # MFI shows buying pressure on the security, buy!
            if mfi[-1] > 50 and mfi[-2] <= 50:
                allocation_dict = {i: 1}

            # MFI opposite direction of price action, signal a reversal, buy!
            if (d[-1][i]['close'] < d[-2][i]['close']) and (mfi[-1] > mfi[-2] > mfi[-3]):
                allocation_dict = {i: 1}

            # MFI is overbought, sell
            if mfi[-1] >= 80:
                allocation_dict = {i: 0}


        return TargetAllocation(allocation_dict)