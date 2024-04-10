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
        for i in self.tickers:
            # get yesterday's price at close
            current_price = d[-1][i]["close"]
            this_sma = SMA(i, d, 50)
            this_rsi = RSI(i, d, 14)

            log(str(current_price))
            log(str(this_sma[-1]))
            log(str(this_rsi[-1]))
            log("---")

            if current_price > this_sma[-1] and this_rsi[-1] <= 30:
                log("trade!")

        return None