from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SOXX"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1hour"

    def has_falling_volume(self, ticker, data):
        return data[-1][ticker]['volume'] < data[-2][ticker]['volume'] < data[-3][ticker]['volume']

    def run(self, data):
        d = data["ohlcv"]
        h = data["holdings"]
        allocation_dict = {} 
        for i in self.tickers:
            bb  = BB(i, d, 14, 1.3)
            rsi = RSI(i, d, 5)
            macd = MACD(i, d, 12, 26)
            current_price_close = d[-1][i]['close']

            log(str(macd[-1]))

            # enter a position if the price closes above the middle of the 
            # bollinger band and has an RSI of 50 or greater. add the position
            # incrementally.
            # if (current_price_close >= bb['mid'][-1]) and rsi[-1] >= 50:
            #     if i in h:
            #         allocation_dict = {i: min(1, h[i]+0.1)}
            #     else:
            #         allocation_dict = {i: 0.1}
            # take profits, sell all if closes above upper bollinger band and has 
            # an RSI of 70 or greater
            # elif (current_price_close >= bb['upper'][-1]) and rsi[-1] >= 70:
            #     allocation_dict = {i: 0}
            # exit position, exit if closes below the lower bollinger band and has falling
            # volume, this attempts to exit the position incrementally but in 20% increments
            # elif (current_price_close <= bb['lower'][-1]) and self.has_falling_volume(i, d):
            #     if i in h:
            #         if h[i] >= 0.1:
            #             allocation_dict = {i: min(0, h[i] - 0.1)}
            #         else:
            #             allocation_dict = {i: 0}
            # else:
            #     allocation_dict = h

        return TargetAllocation(allocation_dict)