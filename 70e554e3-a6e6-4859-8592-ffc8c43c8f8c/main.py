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

    def run(self, data):
        d = data["ohlcv"]
        allocation_dict = {}
        for i in self.tickers:
            bb = BB(i, d, 14, 1)
            
            # entrace
            #
            # if price opens below middle bollinger band and closes above middle band
            if (d[-1][i]['open'] < bb['mid'][-1]) and (d[-1][i]['close'] > bb['mid'][-1]):
                allocation_dict = {i: 1}

            # entrace
            # if (d[-1][i]['close'] > bb['mid'][-1]) and self.has_rising_rsi(i, d):
            #     allocation_dict = {i: 1}
            
            # stop loss
            if (d[-1][i]['close'] < bb['lower'][-1]):
                allocation_dict = {i: 0}

        return TargetAllocation(allocation_dict)