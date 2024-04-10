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
        return data[-1][ticker]["close"] > data[-2][ticker]["close"] > data[-3][ticker]["close"]

    def above_moving_averages(self, ticker, data):
        '''
        check if the price is currently above the 50 and 100
        day moving average
        '''
        50d_sma = SMA(ticker, data, 50)
        100d_sma = SMA(ticker, data, 100)
        return data[-1][ticker]["close"] > 50d_sma[-1] > 100d_sma[-1]

    def run(self, data):
        d = data["ohlcv"]
        allocation_dict = {}

        for i in self.tickers:
            if self.has_momentum(i, d) and self.above_moving_averages(i, d):
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