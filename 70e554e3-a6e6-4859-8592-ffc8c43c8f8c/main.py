from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["QQQ"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        d = data["ohlcv"]
        allocation_dict = {}
        for i in self.tickers:
            bb = BB(i, d, 14, 1)
            rsi = RSI(i, d, 14)

            if (d[-1][i]["close"] > bb['lower'][-1]) and (rsi[-1] >= 50):
                allocation_dict = {i: 1}

            if (d[-1][i]["close"] < bb['lower'][-1]):
                allocation_dict = {i: 0}

        return TargetAllocation(allocation_dict)