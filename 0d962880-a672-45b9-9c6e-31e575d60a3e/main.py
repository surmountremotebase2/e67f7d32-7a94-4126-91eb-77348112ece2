from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log
import pandas_ta as ta
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["QQQ"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"

    def SMAVol(self, ticker, data, length):
        '''Calculate the moving average of trading volume

        :param ticker: a string ticker
        :param data: data as provided from the OHLCV data function
        :param length: the window

        :return: list with float SMA
        '''
        close = [i[ticker]["volume"] for i in data]
        d = ta.sma(pd.Series(close), length=length)
        if d is None:
            return None
        return d.tolist()

    def run(self, data):
        d = data["ohlcv"]
        h = data["holdings"]
        allocation_dict = {} 
        for i in self.tickers:
            current_price_open  = d[-1][i]['open']
            current_price_close = d[-1][i]['close']

            vol_sma_fast = self.SMAVol(i, d, 5)
            vol_sma_slow = self.SMAVol(i, d, 13)

            if vol_sma_fast[-1] > vol_sma_slow[-1]:
                allocation_dict = {i: 1}

            if vol_sma_fast[-1] < vol_sma_slow[-1]:
                allocation_dict = {i: 0}

        return TargetAllocation(allocation_dict)