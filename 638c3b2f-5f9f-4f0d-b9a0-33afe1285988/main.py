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
            log(str(current_price))

            # get the current rsi for each symbol
            this_rsi = RSI(i, d, 14)
            if this_rsi[-1] <= 30:
                log("trade")

        return None