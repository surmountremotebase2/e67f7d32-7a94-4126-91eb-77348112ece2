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

    def has_rising_rsi(self, ticker, data):
        rsi = RSI(ticker, data, 14)
        return (rsi[-1] >= 50) and (rsi[-1] > rsi[-2] > rsi[-3])

    def has_falling_rsi(self, ticker, data):
        rsi = RSI(ticker, data, 14)
        return (rsi[-1] < rsi[-2] < rsi[-3])

    def run(self, data):
        d = data["ohlcv"]
        allocation_dict = {}
        for i in self.tickers:
            bb  = BB(i, d, 14, 1)
            rsi = RSI(i, d, 14)

            current_price_open  = d[-1][i]['open']
            current_price_close = d[-1][i]['close']
            
            # entrace
            #
            # if the current price opened below middle bollinger band and closed above
            # middle bollinger band and also has rising RSI above 50, buy!
            # if (current_price_close > bb['mid'][-1]) \
            #   and self.has_rising_rsi(i, d):
            #     allocation_dict = {i: 1}
            if (current_price_close > bb['mid'][-1]) and rsi[-1] >= 50:
                allocation_dict = {i: 1}
            
            # exit
            #
            # exit position when it closes below the lower bollinger band
            if (current_price_close < bb['lower'][-1]) and self.has_falling_rsi(i, d):
                allocation_dict = {i: 0}

        return TargetAllocation(allocation_dict)