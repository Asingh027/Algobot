# Imports
from queue import Empty
from keys import *
import pandas as pd
import time
import alpaca_trade_api as tradeapi
from termcolor import colored
from stock_price_trend_evaluator import evaluator
import math
import re
from bs4 import BeautifulSoup
import requests
import sys

# Gather S&P 100 tickers from wikipedia


def get_sp_100_dataset():
    sp100 = pd.read_html(
        "https://en.wikipedia.org/wiki/S%26P_100#Components")
    tickers = sp100[2]['Symbol'].values.tolist()
    return tickers


# Gets list of S&P 500 tickers
stocks = get_sp_100_dataset()

# Gets rid of tickers with periods in it, as this messes up the yfinance API
# Removes BRK.B and BF.B
for i in stocks:
    if "." in i:
        stocks.remove(i)


def sell(ticker):
    t = evaluator([ticker])
    x = t.execute()
    temp = x[(x.MACD == 'Sell') & (x.RSI == 'Sell')]
    if temp.empty:
        return False
    else:
        return True


def buy(ticker):
    t = evaluator([ticker])
    x = t.execute()
    temp = x[(x.MACD == 'Buy') & (x.RSI == 'Buy')]
    if temp.empty:
        return False
    else:
        return True


# Connects us to APIs
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL)

# Check Account Status:
ACCOUNT = api.get_account()
print("Your account is " + ACCOUNT.status)
print("Your buying power as of right now is $" +
      colored(ACCOUNT.buying_power, 'green'))
BALANCE_CHANGE = float(ACCOUNT.equity) - float(ACCOUNT.last_equity)
if BALANCE_CHANGE > 0:
    print("Today's portfolio balance change: " +
          colored(str(BALANCE_CHANGE), 'green') + "\n")
elif BALANCE_CHANGE < 0:
    print("Today's portfolio balance change: " +
          colored(str(BALANCE_CHANGE), 'red') + "\n")
else:
    print("Today's portfolio balance change: " +
          colored(str(BALANCE_CHANGE), 'cyan') + "\n")


def is_Open():
    time.sleep(0.5)
    return api.get_clock().is_open


# While market hours
while is_Open():
    # Check current positions
    ORDERS = api.list_positions()
    # If no positions, continue
    if ORDERS == []:
        continue
    else:
        # For each position I'm in
        for i in ORDERS:
            # If both sell conditions are true, we close the position
            if sell(i.symbol) == True:
                api.submit_order(i.symbol, side='sell', type='market')
                print(colored('Confirmed! ', 'yellow') + "You've successfully " +
                      colored("sold ", 'red') + "all shares of " + str(i.symbol) + "!")
                if i.symbol not in stocks:
                    stocks.append(i.symbol)

    # Evaluate stocks for the day
    t = evaluator(stocks)
    x = t.execute()
    temp = x[(x.MACD == 'Buy') & (x.RSI == 'Buy')]
    final = list(temp.index)

    # Buy all stocks given using 50% of buying power

    # Get buying power for this trade
    temp_buy = float(ACCOUNT.buying_power)/2.0

    # For each stock we're gonna buy
    for i in final:
        # get number of shares
        q = (temp_buy/len(final))/(evaluator(
            [i]).fetch_data(i).iloc[-1, 3])

        # Submit market order for shares of stock
        api.submit_order(symbol=i, qty=q, side='buy', type='market')

        # Pring confirmation message
        print(colored('Confirmed! ', 'yellow') + "You've successfully " +
              colored("bought ", 'green') + str(q) + " shares of " + str(i) + "! I'm now removing it from stocks so we can't buy it again today. ")

        # We're removing this stock from the stocks list so that we can't keep buying it every 60 seconds
        # Once we sell this position, it'll get re-added.
        stocks.remove(i)

    else:
        print("No change in evaluation!")

    # wait 60 seconds
    print("\nWaiting 60 seconds")
    for timer in range(15, 60, 15):
        time.sleep(15)
        print(str(60 - timer) + " seconds left.")

# While not market hours
if not is_Open():
    stocks = get_sp_100_dataset()
    print('Stocks list re-updated')
    CURRENT_TIME = time.strftime("%H:%M:%S", time.localtime())
    print("The market isn't open yet. The current time is " +
          colored(CURRENT_TIME, 'cyan') + ".")
    print("Waiting 1 hour")
    time.sleep(3600)
    print("Rerunning Algorithm")
    sys.runfile('main.py')
