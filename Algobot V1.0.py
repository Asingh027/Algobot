# Imports
import time
import alpaca_trade_api as tradeapi
from keys import API_KEY, API_SECRET, APCA_API_BASE_URL
from termcolor import colored


# Stocks we are using
STOCK_DATABASE = ["SPY"]

# Connects us to APIs
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL)
AV = api.alpha_vantage

# FUNCTIONS
# Returns a boolean on whether or not the market is open


def is_Open():
    return api.get_clock().is_open


api.get_clock().is_open

# Calculates Moving Average with a certain lag


def movingAverage(symbol, lag, data):
    close = data["4. close"]
    return sum(close[0:lag])/lag

# Checks to see if our account is holding a position


def is_position(ticker):
    try:
        api.get_position(ticker)
    except:
        return False
    return True


# Check Account Status:
ACCOUNT = api.get_account()
print("Your account is " + ACCOUNT.status)
print("Your buying power as of right now is $" + ACCOUNT.buying_power)
BALANCE_CHANGE = float(ACCOUNT.equity) - float(ACCOUNT.last_equity)
print("Today's portfolio balance change: " + str(BALANCE_CHANGE) + "\n")

if not is_Open():
    CURRENT_TIME = time.strftime("%H:%M:%S", time.localtime())
    print("The market isn't open yet. The current time is " +
          colored(CURRENT_TIME, 'cyan') + ".")
    print("Waiting 30 minutes")
    time.sleep(1800)
    print("Rerunning Algorithm")
    runfile('Algobot.py')

while is_Open():
    for ticker in STOCK_DATABASE:
        data = AV.intraday_quotes(
            ticker, interval='1min', outputsize="full", output_format="pandas")
        max_buy = int(float(ACCOUNT.buying_power)/float(data["4. close"][0]))

        # Calculate 5-minute Moving Average
        rolling_mean_5 = movingAverage(ticker, 5, data)
        print(ticker + ": Moving Average with a lag of 5 computed to be " +
              colored(str(rolling_mean_5), color='cyan') + ".")

        # Calculate 20-minute Moving Average
        rolling_mean_20 = movingAverage(ticker, 20, data)
        print(ticker + ": Moving Average with a lag of 20 computed to be " +
              colored(str(rolling_mean_20), color='cyan') + ".\n")

        # Calculate Difference between moving averages
        diff = (rolling_mean_5 - rolling_mean_20) > 0

        if diff:
            print(ticker + ": The 5 moving average is above the 20 moving average. \n")
            if is_position(ticker):
                api.submit_order(ticker, qty=max_buy, side="sell",
                                 type='market', time_in_force="day")
                print(colored("Selling 1 share of " + ticker + ". \n", color='red'))
        if not diff:
            print(ticker + ": The 5 moving average is " +
                  colored("NOT", 'red') + " above the 20 moving average. \n")
            if not is_position(ticker):
                api.submit_order(ticker, qty=max_buy, side="buy",
                                 type='market', time_in_force="day")
                print(colored("Buying 1 share of " +
                      ticker + ". \n", color='green'))

    print("Waiting 60 seconds \n")
    for timer in [15, 30, 45, 60]:
        time.sleep(15)
        print(str(60 - timer) + " seconds left \n")
