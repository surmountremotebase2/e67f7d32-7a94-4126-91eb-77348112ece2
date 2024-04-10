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
            # get yesterday's price at close
            current_price = d[-1][i]["close"]
            log(current_rice)

            # get the current rsi for each symbol
            this_rsi = RSI(i, d, 14)

            if this_rsi[-1] <= 30:
                #if this_rsi[-1] < this_rsi[0]:
                log("trade")

            # log(str(this_rsi[-1]))
            # log(str(this_rsi[-2]))
            # log(str(this_rsi[-3]))
            #if (this_sma[-1] > this_sma[-2]) && (this_rsi <= 30):
                #log("trade.")
                #return TargetAllocation(allocation_dict)

        return None