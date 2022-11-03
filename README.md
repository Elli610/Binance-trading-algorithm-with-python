# Binance-trading-algorithm-with-python

Last year, I built a trading algorithm with python and binance API. In this repository, you can see each version of my algorithm. Enjoy !


## How to use the algorithm 

You will need the following libraries: 
- python-binance
- talib (This library was not accessible with pip. Choose the version corresponding to your configuration online)
- sqlite3


- Start by generating an api key on binance then allow spot trading for this key. Then copy the api key and the secret key into the config.ini file.

- In this file, choose your parameters (I advise you to stay on 1 minute intervals, I have bugs on the other intervals).

- Choose the pair to trade

- Choose the indicators that interest you

WARNING: the simple strategy mode is not yet 100% functional. Be careful. I recommend leaving it at 0.



## ROI and usefull informations

I ran this algorithm from May 2021 to July 2021 constantly on the BTC/USDT pair and lost 1 usd.
He was very efficient when prices were going up and lost a lot when prices were going down quickly.

I plan today to create a test mode to allow you to test it without gambling your money.

Either way, be careful. This algorithm is a tool that you can use but I don't guarantee any gain and I can't assure you that you won't lose anything.

You are free to use and modify this algorithm for your own benefit, but it is not to be sold.

