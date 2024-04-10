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

    def has_momentum(self, ticker, data):
        '''
        check if the ticker provided has 3 days of closes consecutively 
        above the previous days, this shows some sort of momentum
        '''
        d = data["ohlcv"]
        return d[-1][ticker]["close"] > d[-2][ticker]["close"] > d[-3][ticker]["close"]

    def run(self, data):
        d = data["ohlcv"]
        allocation_dict = {}

        for i in self.tickers:
            if self.has_momentum(i, d):
                log("MOMENTUM!")

        # for i in self.tickers:
        #     current_price = d[-1][i]["close"]
        #     fifty_day_sma = SMA(i, d, 50)
        #     two_hundy_day_sma = SMA(i, d, 200)
        #     if (current_price > fifty_day_sma[-1]) and (fifty_day_sma[-1] > two_hundy_day_sma[-1]):
        #         allocation_dict[i] = 1

        #     if (current_price < fifty_day_sma[-1] < two_hundy_day_sma[-1]):
        #         allocation_dict[i] = 0

        return TargetAllocation(allocation_dict)