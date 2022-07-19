# Imports
import timeit
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta

# TRY THIS PACKAGE
from stock_indicators import indicators as ind

# Gather S&P 500 tickers from wikipedia


def get_sp_500_dataset():
    sp500 = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    tickers = sp500[0]['Symbol'].values.tolist()
    return tickers


# Gets list of S&P 500 tickers
stocks = get_sp_500_dataset()

# Gets rid of tickers with periods in it, as this messes up the yfinance API
# Removes BRK.B and BF.B
for i in stocks:
    if "." in i:
        stocks.remove(i)


# Our mini stock database and current indicators
ministonk = ['AAPL', 'GOOGL', 'MSFT', 'FB', 'TSLA']
inds = ["MACD", "RSI", "Bollinger Bands"]


class evaluator:
    def __init__(self, tickers):
        self.tickers = tickers

    def fetch_data(self, ticker):
        global df
        df = yf.Ticker(ticker).history(start=date.today() -
                                       relativedelta(months=1), end=date.today())
        return df

    def MACD(self, price, slow=26, fast=12, smooth=9):
        # Finds the exponential weighted means for the two signal lines
        exp1 = price.ewm(span=fast, adjust=False).mean()
        exp2 = price.ewm(span=slow, adjust=False).mean()

        # Computes the difference and labels it MACD
        macd = exp1 - exp2

        # Computes the signal line which we'll compare to the MACD
        signal = macd.ewm(span=smooth, adjust=False).mean()

        # Computes the difference between the two.
        trend = macd - signal

        # Adds new column that finds the direction of the difference line.
        diff = np.diff(trend)

        # If slope of the signal line is positive AND the difference between the 2 lines is positive, we BUY
        if diff[-1] > 0 and trend[-1] > 0:
            return True

        # If slope of the signal line is negative OR the difference between the 2 lines is negative, we SELL
        elif diff[-1] < 0 or trend[-1] < 0:
            return False

        else:
            return np.NaN

    def RSI(self, df):
        # Calculate the RSI

        # Look for crosses

        # Recommend accordingly
        return np.NaN

    def BOL(self, df):
        # Calculate the Bollinger Bands

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


t = evaluator(ministonk)

print(t.execute())

# print(ind.get_macd(df['Close']))

#test = yf.Ticker("AAPL")

# print(test.history())

#t2 = test.financials

# print(t2)

#print(t2.loc["Net Income"])

# Use this function to check efficiency of code


def timer():
    start = timeit.default_timer()

    # Your statements here
    t = evaluator(stocks[0:50])

    print(t.execute())

    stop = timeit.default_timer()

    print('Time: ', stop - start)

    start = timeit.default_timer()

    # Your statements here

    t = evaluator(stocks[0:50])

    print(t.execute())

    stop = timeit.default_timer()

    print('Time: ', stop - start)


# print(timer())
