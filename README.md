# Welcome to my Algobot Project! 
### Check out the files below:
#### [Algobot V1.0.py](https://github.com/Asingh027/Algobot/blob/master/Algobot%20V1.0.py)

This file was the original code I implemented in 2020, when I first started this project. I recently rediscovered the code from deep in my folders and decided to revamp it with my newfound data science skills! The original code utilized the 5-day Moving Average and the 20-day Moving Average to indicate buy or sell signals, then pushed these evaluations as buy or sell orders via the Alpaca API. It re-evaluates the stock price every minute and sells if it detects a negative trend.  

#### [main.py](https://github.com/Asingh027/Algobot/blob/master/main.py) 
:warning: _WIP_ :warning:

This is the main Algobot file, which will contain the meat and potatoes of the project. This entails pushing API requests to Alpaca. I plan to make another file that will recommend stocks to the algorithm. A couple ideas I had for recommending stocks include: 

<ul>
  <li>Analyst Recommendation</li>
  <li>Social Media Sentiment Analysis</li>
  <li>Classification model - Involves training model on backtested trading signals then predicting buy trends </li>
</ul>

analyst recommendations, Social Media Sentiment Analysis, classification. 

#### [scrape_indicators.py](https://github.com/Asingh027/Algobot/blob/master/scrape_indicators.py) 
:warning: _WIP_ :warning: 

This file holds a function I made that scrapes crucial financial information from Yahoo! Finance and stores it in a dictionary. If I plan to use this function, I'll import it into main.py, but for now, I don't plan to implement it into my main program. 

#### [stock_price_trend_evaluator.py](https://github.com/Asingh027/Algobot/blob/master/stock_price_trend_evaluator.py)
:warning: _WIP_ :warning:

This file contains a class indicators which takes in a list of tickers, fetches the historical price data, then calculates each selected indicator's value. Once these calculations are done, the class's execute function runs, which appends the final recommendation based on each signal to a pandas DataFrame object. The recommendation takes form as a True/False value, where True indicates Buy and False indicates Sell. As the model evolves and I conduct research on better trading signals, my strategy will continue to improve! The current indicators I am implementing are: 

<ul>
  <li>MACD - Moving Average Convergence Divergence</li>
  <li>RSI - Relative Strength Index</li>
  <li>Bollinger Bands</li>
  <li>Super Trend</li>
</ul>
