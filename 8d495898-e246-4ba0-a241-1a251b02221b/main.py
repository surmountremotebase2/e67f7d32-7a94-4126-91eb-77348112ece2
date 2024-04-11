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

    def has_bottom_reversal(self, ticker, data):
        '''
        if the fast EMA crosses over the slow EMA
        '''
        ema_fast = EMA(ticker, data, 7)
        ema_slow = EMA(ticker, data, 14)
        return (ema_fast[-1] > ema_slow[-1]) and \
               (ema_fast[-2] < ema_slow[-2]) and \
               (ema_fast[-3] < ema_slow[-3])

    def has_top_reversal(self, ticker, data):
        '''
        if the slow EMA crosses over the fast EMA
        '''
        ema_fast = EMA(ticker, data, 7)
        ema_slow = EMA(ticker, data, 14)
        return (ema_fast[-1] < ema_slow[-1]) and \
               (ema_fast[-2] > ema_slow[-2]) and \
               (ema_fast[-3] > ema_slow[-3])

    def run(self, data):
        d = data["ohlcv"]
        allocation_dict = {}

        # this assumes that there is only one ticker because of
        # how the allocation_dict logic works, this would need 
        # to be fixed to support multiple tickers truly
        for i in self.tickers:
            if self.has_bottom_reversal(i, d):
                allocation_dict = {i: 1}

            if self.has_top_reversal(i, d):
                allocation_dict = {i: 0}

        return TargetAllocation(allocation_dict)