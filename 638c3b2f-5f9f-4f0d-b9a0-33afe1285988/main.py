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
        return "1day"

    def run(self, data):
        d = data["ohlcv"]
        allocation_dict = {}
        for i in self.tickers:
            current_price = d[-1][i]["close"]
            this_sma = SMA(i, d, 50)
            this_rsi = RSI(i, d, 14)
            if current_price > this_sma[-1]:
                allocation_dict.append({i: 1})

        # self.count += 1
        # if (self.count % 30 == 1):
        #     allocation_dict = {self.tickers[i]: self.weights[i]/sum(self.weights) for i in range(len(self.tickers))}
        #     return TargetAllocation(allocation_dict)

        return TargetAllocation(allocation_dict)