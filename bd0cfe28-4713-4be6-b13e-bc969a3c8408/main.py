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

    # def has_falling_volume(self, ticker, data):
    #     return data[-1][ticker]['volume'] < data[-2][ticker]['volume'] < data[-3][ticker]['volume']

    def run(self, data):
        d = data["ohlcv"]
        h = data["holdings"]
        allocation_dict = {} 
        for i in self.tickers:
            if len(data)<20:
                return TargetAllocation({})
            
            bb  = BB(i, d, 20, 1.4)
            rsi = RSI(i, d, 2)
            current_price_close = d[-1][i]['close']

            if (current_price_close > bb['mid'][-1]) and rsi[-1] >= 50:
                if h[i] >= 0:
                    allocation_dict = {i: min(1, h[i]+0.1)}
                else:
                    allocation_dict = {i: 0.4}
            elif (current_price_close > bb['upper'][-1]):
                if h[i] > 0:
                    allocation_dict = {i: min(1, h[i]-0.1)}
                else:
                    allocation_dict = {i: 0}
            else:
                allocation_dict = {i: 0}

        return TargetAllocation(allocation_dict)