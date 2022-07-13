# Imports
import pandas as pd
import numpy as np
from IPython.display import display
import yfinance as yf

# Gather S&P 500 tickers from wikipedia


def get_sp_500_dataset():
    sp500 = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    tickers = sp500[0]['Symbol'].values.tolist()
    return tickers


# stocks = get_sp_500_dataset()

ministonk = ['AAPL', 'GOOGL', 'MSFT', 'FB', 'TSLA']
inds = ["MACD", "RSI", "Bollinger Bands", "Super Trend"]
# CLASS THAT TAKES TICKER AND SPITS OUT INDICATOR'S EVALUATION OF IT

ind = []


class indicators:

    def __init__(self, tickers):
        self.tickers = tickers

    def fetch_data(self, ticker):
        return yf.Ticker(ticker).history(period="max")

    def MACD(self):
        # Calculate the MACD

        # Look for crosses

        # Recommend accordingly
        return True

    def RSI(self):
        # Calculate the RSI

        # Look for crosses

        # Recommend accordingly
        return True

    def BOL(self):
        # Calculate the MACD

        # Look for signals

        # Recommend accordingly
        return True

    def SuperTrend(self):
        # Calculate the MACD

        # Look for trends

        # Recommend accordingly
        return True

    def execute(self):
        result_df = pd.DataFrame()
        for ticker in self.tickers:
            # df = self.fetch_data(ticker)

            result_df[ticker] = [self.MACD(),
                                 self.RSI(), self.BOL(), self.SuperTrend()]

        result_df = result_df.transpose()
        result_df.columns = inds
        return result_df


t = indicators(ministonk)

# print(t.execute())

test = yf.Ticker("AAPL")

t2 = test.financials

print(t2)

print(t2.loc["Net Income"])

# Find top buy stocks and buy them

# Find top sell stocks and sell if we have a position in it
