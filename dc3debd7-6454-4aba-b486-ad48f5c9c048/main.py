from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset this strategy will operate on
        self.ticker = "VTI"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # Define the interval for data; 1 day for daily moving average and RSI levels
        return "1day"

    def run(self, data):
        sma50 = SMA(self.ticker, data["ohlcv"], 50)  # 50-day Simple Moving Average
        rsi = RSI(self.ticker, data["ohlcv"], 14)  # 14-day Relative Strength Index

        if not sma50 or not rsi:
            log("Insufficient data for SMA or RSI calculation.")
            return TargetAllocation({self.ticker: 0})  # Return zero allocation if data is insufficient

        current_price = data["ohlcv"][-1][self.ticker]["close"]
        latest_sma50 = sma50[-1]
        latest_rsi = rsi[-1]
        
        allocation = 0  # Default to 0 allocation

        # Buy condition: Price is above 50-day SMA and RSI is below 35
        if current_price > latest_sma50 and latest_rsi < 35:
            log(f"Buy signal triggered for {self.ticker}.")
            allocation = 1  # Full allocation

        # Sell condition: Price crosses below 50-day SMA and RSI is above 70
        elif current_price < latest_sma50 and latest_rsi > 70:
            log(f"Sell signal triggered for {self.ticker}.")
            allocation = 0  # Zero allocation reflecting a sell decision

        return TargetAllocation({self.ticker: allocation})