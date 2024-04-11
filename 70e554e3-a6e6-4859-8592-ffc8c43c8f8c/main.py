from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY", "QQQ", "VTI"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "4hour"

    def run(self, data):
        d = data["ohlcv"]
        allocation_dict = {}
        for i in self.tickers:

        return TargetAllocation(allocation_dict)