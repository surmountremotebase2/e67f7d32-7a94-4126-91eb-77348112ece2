from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY", "QQQ"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1hour"

    def run(self, data):
        d = data["ohlcv"]
        for i in self.tickers:
            this_sma = SMA(i, d, 5)
            this_rsi = RSI(i, d, 14)
            if (this_sma[-1] > this_sma[-2]) && (this_rsi <= 30):
                log("trade.")
                #return TargetAllocation(allocation_dict)
        return None