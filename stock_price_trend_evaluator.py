# Imports
from keys import *
import timeit
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from dateutil.relativedelta import relativedelta
import requests
import csv


def get_sp_100_dataset():
    sp100 = pd.read_html(
        "https://en.wikipedia.org/wiki/S%26P_100#Components")
    tickers = sp100[2]['Symbol'].values.tolist()
    return tickers


# Our mini stock database and current indicators
ministonk = ['TSLA', 'AAPL', 'AMZN', 'MSFT']
inds = ["MACD", "RSI", "BolBands"]

stocks = get_sp_100_dataset()

for i in stocks:
    if "." in i:
        stocks.remove(i)


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
        df = yf.Ticker(ticker).history(start=datetime.date.today() -
                                       relativedelta(months=3), end=datetime.date.today())
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
        print(trend[-1])
        # print(diff)

        # If slope of the signal line is positive AND the difference between the 2 lines is positive, we BUY
        if trend[-1] > 0:
            return 'Buy'

        # If slope of the signal line is negative OR the difference between the 2 lines is negative, we SELL
        elif trend[-1] < 0:
            return 'Sell'

    def RSI(self, close, periods=14, low=30, high=70):
        ret = close.diff()
        up = []
        down = []
        for i in range(len(ret)):
            if ret[i] < 0:
                up.append(0)
                down.append(ret[i])
            else:
                up.append(ret[i])
                down.append(0)
        up_series = pd.Series(up)
        down_series = pd.Series(down).abs()
        up_ewm = up_series.ewm(com=periods - 1, adjust=False).mean()
        down_ewm = down_series.ewm(com=periods - 1, adjust=False).mean()
        rs = up_ewm/down_ewm
        rsi = 100 - (100 / (1 + rs))
        rsi_df = pd.DataFrame(rsi).rename(
            columns={0: 'RSI'}).set_index(close.index)
        rsi_df = rsi_df.dropna()
        final = rsi_df[3:].RSI
        print(final[-1])
        # print(final.index[-1])

        if final[-1] <= low:
            return 'Buy'

        elif final[-1] >= high:
            return 'Sell'

        else:
            return 'Hold'

    def Bollinger(self, prices, rate=20):
        sma = prices.rolling(rate).mean()
        std = prices.rolling(rate).std()
        up = sma + std * 2  # Calculate top band
        down = sma - std * 2  # Calculate bottom band
        if prices[-1] < down[-1]:
            return 'Buy'
        elif prices[-1] > up[-1]:
            return 'Sell'
        else:
            return 'Hold'

    def execute(self):
        result_df = pd.DataFrame()
        for ticker in self.tickers:
            df = self.fetch_data(ticker)
            print(ticker)
            result_df = pd.concat((result_df, pd.Series([self.MACD(df['Close']), self.RSI(
                df['Close'], low=30, high=70), self.Bollinger(df['Close'])])), axis=1)
            print('------------------------')
        result_df = result_df.transpose()
        result_df.columns = inds
        result_df.index = self.tickers
        # print(result_df)
        return result_df


ministonk = ['TSLA', 'AAPL', 'AMZN', 'MSFT', 'T']

t = evaluator(stocks)
x = t.execute()
print(x)
temp = pd.DataFrame()
for i in x.T:
    if sum((x.loc[[i]] == 'Buy').values.flatten().tolist()) >= 2:
        temp = pd.concat((temp, pd.Series([x.loc[[i]]])), axis=1)
        #temp = x[(x.MACD == 'Buy') | (x.RSI == 'Buy') | (x.BolBands == 'Buy')]
print(temp)
final = list(temp.index)
# MAJORITY

# for i in ministonk:
#    if sum((x.loc[[i]] == 'Buy').values.flatten().tolist()) >= 2:
#        print(True)
#    else:
#        print(False)

#    if ((x.loc[[i]] == 'Buy').sum(axis=1) >= 2):
#        print(i)


# t = evaluator(['AMGN']).fetch_data('AMGN').iloc[-1, 3]
# print(t)
# x = t.fetch_data('AMGN')
# print(x.iloc[-1, 3])

# x = t.fetch_data('AAPL')

# print(x)


# print(temp.index)

# print(x)

# print(t.RSI(df))

# print(ind.get_macd(df['Close']))

# test = yf.Ticker("AAPL")

# print(test.history(interval='1m', start=datetime.date.today() - datetime.timedelta(days=7), end=datetime.date.today()))

# t2 = test.financials

# print(t2)

# print(t2.loc["Net Income"])

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

    t = evaluator(stocks[:50])

    print(t.execute2())

    stop = timeit.default_timer()

    print('Time: ', stop - start)


# print(timer())
