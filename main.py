# Imports
from keys import *
import time
import alpaca_trade_api as tradeapi
from termcolor import colored
import re
from bs4 import BeautifulSoup
import requests
import sys

# Stocks we are using
STOCK_DATABASE = ["SPY"]

# Connects us to APIs
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL)

# FUNCTIONS
"""
# Returns a boolean on whether or not the market is open
def is_Open():
    return api.get_clock().is_open

# Checks to see if our account is holding a position
def is_position(ticker):
    try:
        api.get_position(ticker)
    except:
        return False
    return True
"""

# Check Account Status:
ACCOUNT = api.get_account()
print("Your account is " + ACCOUNT.status)
print("Your buying power as of right now is $" + ACCOUNT.buying_power)
BALANCE_CHANGE = float(ACCOUNT.equity) - float(ACCOUNT.last_equity)
print("Today's portfolio balance change: " + str(BALANCE_CHANGE) + "\n")
""""""
# if not is_Open():


#CURRENT_TIME = time.strftime("%H:%M:%S", time.localtime())
#print("The market isn't open yet. The current time is " + colored(CURRENT_TIME, 'cyan') + ".")
#print("Waiting 30 minutes")
# time.sleep(1800)
#print("Rerunning Algorithm")
# runfile('Algobot.py')

while is_Open():
    for ticker in STOCK_DATABASE:
        data = AV.intraday_quotes(
            ticker, interval='1min', outputsize="full", output_format="pandas")
        max_buy = int(float(ACCOUNT.buying_power)/float(data["4. close"][0]))

        # Initialize stock list
        Stonks = []

        # Check for companies with beta between 0.9 and 1.1

        # Check EPS for profitability

        # Check for Low Debt-equity Ratio

        # Once passes all parameters, add to stock list

        # If stock price goes down by 10%, buy

        # Sell after 5% profit

    print("Waiting 60 seconds \n")
    for timer in [15, 30, 45, 60]:
        time.sleep(15)
        print(str(60 - timer) + " seconds left \n")
