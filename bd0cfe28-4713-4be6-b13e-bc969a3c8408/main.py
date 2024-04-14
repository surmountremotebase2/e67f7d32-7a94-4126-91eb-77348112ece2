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
        h = data["holdings"]
        allocation_dict = {} 

        log(str(h))

        for i in self.tickers:
            bb  = BB(i, d, 20, 1.4)
            rsi = RSI(i, d, 2)
            current_price_close = d[-1][i]['close']

            if (current_price_close >= bb['mid'][-1]) and rsi[-1] >= 50:
                log("buy")
                if i in h:
                    allocation_dict = {i: min(1, h[i]+0.1)}
                else:
                    allocation_dict = {i: 0.1}
            elif (current_price_close >= bb['upper'][-1]):
                log("sell")
                if i in h:
                    if h[i] > 0:
                        allocation_dict = {i: min(1, h[i]-0.1)}
            else:
                log("empty")

        return TargetAllocation(allocation_dict)