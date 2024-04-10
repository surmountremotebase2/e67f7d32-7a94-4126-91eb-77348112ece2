from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY", "QQQ"]
        #self.tickers = ["MNDY", "TTD", "OKTA", "ROKU"]

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
        return data[-1][ticker]["close"] > \
               data[-2][ticker]["close"] > \
               data[-3][ticker]["close"]

    def has_decelerated(self, ticker, data):
        '''
        check if the security has decelerated over the past
        few days
        '''
        return data[-1][ticker]["close"] < \
               data[-2][ticker]["close"] < \
               data[-3][ticker]["close"]

    def above_moving_averages(self, ticker, data):
        '''
        check if the price is currently above the 21 day EMA
        and that is above the 50 day SMA. this informs us if
        we are buying into strength.
        '''
        my_ema = EMA(ticker, data, 21)
        my_sma = SMA(ticker, data, 50)
        return data[-1][ticker]["close"] > my_ema[-1] > my_sma[-1]

    def below_moving_averages(self, ticker, data):
        '''
        check if the current price is below the 21 day EMA
        and that it is still above the 50 day SMA. this may mean
        we are seeing a downward trend start.
        '''
        my_ema = EMA(ticker, data, 21)
        my_sma = SMA(ticker, data, 50)
        return data[-1][ticker]["close"] < my_ema[-1] > my_sma[-1]
    
    def is_overbought(self, ticker, data):
        '''
        determine if security is overbought using RSI
        as a metric
        '''
        rsi = RSI(ticker, data, 14)
        return rsi[-1] >= 70

    def run(self, data):
        d = data["ohlcv"]
        allocation_dict = {}

        for i in self.tickers:
            if self.has_momentum(i, d) and self.above_moving_averages(i, d):
                allocation_dict[i] = 1

            if self.is_overbought(i, d) and \
               self.has_decelerated(i, d) and \
               self.below_moving_averages(i, d):
                allocation_dict[i] = 0

        # for i in self.tickers:
        #     current_price = d[-1][i]["close"]
        #     fifty_day_sma = SMA(i, d, 50)
        #     two_hundy_day_sma = SMA(i, d, 200)
        #     if (current_price > fifty_day_sma[-1]) and (fifty_day_sma[-1] > two_hundy_day_sma[-1]):
        #         allocation_dict[i] = 1

        #     if (current_price < fifty_day_sma[-1] < two_hundy_day_sma[-1]):
        #         allocation_dict[i] = 0

        return TargetAllocation(allocation_dict)