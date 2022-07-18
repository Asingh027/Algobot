# Imports
import pandas as pd
import numpy as np
from IPython.display import display
import yfinance as yf

# TRY THIS PACKAGE
from stock_indicators import indicators as ind

# Gather S&P 500 tickers from wikipedia


def get_sp_500_dataset():
    sp500 = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    tickers = sp500[0]['Symbol'].values.tolist()
    return tickers

# stocks = get_sp_500_dataset()


ministonk = ['AAPL', 'GOOGL', 'MSFT', 'FB', 'TSLA']
inds = ["MACD", "RSI", "Bollinger Bands"]


class evaluator:
    def __init__(self, tickers):
        self.tickers = tickers

    def fetch_data(self, ticker):
        global df
        df = yf.Ticker(ticker).history(period="max")
        return df

    def MACD(self, price, slow=26, fast=12, smooth=9):
        # Finds the exponential weighted means for the two signal lines
        exp1 = price.ewm(span=fast, adjust=False).mean()
        exp2 = price.ewm(span=slow, adjust=False).mean()

        # Computes the difference and labels it MACD
        macd = pd.DataFrame(exp1 - exp2)

        # Computes the signal line which we'll compare to the MACD
        signal = pd.DataFrame(macd.ewm(span=smooth, adjust=False).mean())

        # Computes the difference between the two.
        hist = pd.DataFrame(macd - signal)

        # Formatting
        frames = [macd, signal, hist]
        df = pd.concat(frames, join='inner', axis=1)
        df.columns = ['MACD', 'Signal', 'Trend']

        # Adds new column that finds the direction of the difference line.
        df['Diff'] = np.append([0], np.diff(df['Trend']))

        # If slope of the signal line is positive AND the difference between the 2 lines is positive, we BUY
        if df['Diff'][-1] > 0 and df['Trend'][-1] > 0:
            return True

        # If slope of the signal line is negative OR the difference between the 2 lines is negative, we SELL
        if df['Diff'][-1] < 0 or df['Trend'][-1] < 0:
            return False

    def RSI(self, df):
        # Calculate the RSI

        # Look for crosses

        # Recommend accordingly
        return np.NaN

    def BOL(self, df):
        # Calculate the MACD

        # Look for signals

        # Recommend accordingly
        return np.NaN

    def execute(self):
        result_df = pd.DataFrame()
        for ticker in self.tickers:
            df = self.fetch_data(ticker)
            result_df[ticker] = [self.MACD(df['Close']),
                                 self.RSI(df), self.BOL(df)]

        result_df = result_df.transpose()
        result_df.columns = inds
        return result_df


def test():
    t = evaluator(ministonk)

    df = t.fetch_data('GOOGL')

    close = df['Close']

    print(t.MACD(close))
    return


t = evaluator(ministonk)

print(t.execute())

# print(ind.get_macd(df['Close']))

#test = yf.Ticker("AAPL")

# print(test.history())

#t2 = test.financials

# print(t2)

#print(t2.loc["Net Income"])

# Find top buy stocks and buy them

# Find top sell stocks and sell if we have a position in it
