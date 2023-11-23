from AlgorithmImports import *

class ImprovedStrategy(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetCash(100000)


        # Adding equities for the specified companies
        self.AddEquity("JNJ", Resolution.Daily)
        self.AddEquity("MSFT", Resolution.Daily)
        self.AddEquity("PG", Resolution.Daily)
        self.AddEquity("TSLA", Resolution.Daily)


        # Moving averages parameters
        self.short_window = 50
        self.long_window = 200


        # RSI parameters
        self.rsi_period = 14
        self.rsi_threshold_low = 30
        self.rsi_threshold_high = 70


        # Initialize indicators for moving averages and RSI for each equity
        self.sma_short = {}
        self.sma_long = {}
        self.rsi = {}
        self.invested_rsi = {}


        for symbol in ["JNJ", "MSFT", "PG", "TSLA"]:
            self.sma_short[symbol] = self.SMA(symbol, self.short_window, Resolution.Daily)
            self.sma_long[symbol] = self.SMA(symbol, self.long_window, Resolution.Daily)
            self.rsi[symbol] = self.RSI(symbol, self.rsi_period, MovingAverageType.Wilders, Resolution.Daily)
            self.invested_rsi[symbol] = False


    def OnData(self, data):
        for symbol in ["JNJ", "MSFT", "PG", "TSLA"]:
            if not (self.sma_short[symbol].IsReady and self.sma_long[symbol].IsReady and self.rsi[symbol].IsReady):
                return


            price = self.Securities[symbol].Price


            # RSI-based strategy for each equity
            if self.rsi[symbol].Current.Value < self.rsi_threshold_low and not self.invested_rsi[symbol]:
                self.SetHoldings(symbol, 1)
                self.invested_rsi[symbol] = True
                self.Debug(f"Buy Signal (RSI strategy) for {symbol}")


            elif self.rsi[symbol].Current.Value > self.rsi_threshold_high and self.invested_rsi[symbol]:
                self.Liquidate(symbol)
                self.invested_rsi[symbol] = False
                self.Debug(f"Sell Signal (RSI strategy) for {symbol}")


            # Stop-loss for RSI-based strategy for each equity
            if self.invested_rsi[symbol] and self.Portfolio[symbol].AveragePrice != 0 and price / self.Portfolio[symbol].AveragePrice - 1 < -0.05:
                self.Liquidate(symbol)
                self.invested_rsi[symbol] = False
                self.Debug(f"Stop Loss Hit (RSI strategy) for {symbol}")


    def OnEndOfDay(self):
        for symbol in ["JNJ", "MSFT", "PG", "TSLA"]:
            self.Debug(f"RSI ({symbol}): {self.rsi[symbol].Current.Value}")
