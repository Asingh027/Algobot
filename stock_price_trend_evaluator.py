# Imports
from stock_indicators import indicators as ind
from keys import *
import timeit
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta
import requests
import csv

# TRY THIS PACKAGE

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
ministonk = ['TSLA', 'AAPL', 'AMZN', 'MSFT', 'FB']
inds = ["MACD", "RSI", "Bollinger Bands"]


class evaluator:
    def __init__(self, tickers):
        self.tickers = tickers

    def AV_fetch_data(self, ticker, interval='1min', function='TIME_SERIES_INTRADAY_EXTENDED'):
        CSV_URL = 'https://www.alphavantage.co/query?function=' + function + \
            '&symbol=' + ticker + \
            '&interval=' + interval + \
            '&apikey=' + AV_KEY + \
            'datatype=json'

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            data = []
            for row in my_list:
                data.append(row)
            data = pd.DataFrame(data[1:], columns=map(str.title, data[0]))
        return data

    def fetch_data(self, ticker):
        global df
        df = yf.Ticker(ticker).history(start=date.today() -
                                       relativedelta(weeks=1), end=date.today())
        return pd.DataFrame(df)

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
            return 'Buy'

        # If slope of the signal line is negative OR the difference between the 2 lines is negative, we SELL
        elif diff[-1] < 0 or trend[-1] < 0:
            return 'Sell'

        else:
            return 'Hold'

    def RSI(self, df, periods=14, low=30, high=70):
        # Calculate the RSI
        close_delta = df['Close'].diff()

        # Make two series: one for lower closes and one for higher closes
        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)

        ma_up = up.ewm(com=periods - 1, adjust=True,
                       min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, adjust=True,
                           min_periods=periods).mean()

        rsi = ma_up / ma_down
        rsi = 100 - (100/(1 + rsi))

        if rsi[-1] > high:
            return 'Buy'

        elif rsi[-1] < low:
            return 'Sell'

        else:
            return 'Hold'

    def BOL(self, df):

        return np.NaN

    def execute(self):
        result_df = pd.DataFrame()
        for ticker in self.tickers:
            df = self.fetch_data(ticker)
            result_df = pd.concat((result_df, pd.Series([self.MACD(df['Close']), self.RSI(
                df, low=40, high=60), self.BOL(df)])), axis=1)

        result_df = result_df.transpose()
        result_df.columns = inds
        result_df.index = self.tickers
        return result_df


# print(df)

#df = t.fetch_data('MSFT')

# print(t.RSI(df))

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
    t = evaluator(stocks)

    print(t.execute())

    stop = timeit.default_timer()

    print('Time: ', stop - start)

    start = timeit.default_timer()

    # Your statements here

    t = evaluator(stocks)

    print(t.execute2())

    stop = timeit.default_timer()

    print('Time: ', stop - start)


# print(timer())
