import time
from datetime import datetime
import pandas as pd
import numpy as np
from binance.client import Client
#from wazirx_sapi_client.rest import Client
import ccxt
import talib
from config import *
import buy_sell as bs
import sql
import bollingerbandsV3 as bb
import statistics as stat
import pattern_recognition as pr


# Initialize Variables
CANDLE_DURATION_IN_MIN = candle_duration

RSI_PERIOD = period
RSI_OVERBOUGHT = overbought
RSI_OVERSOLD = oversold

CCXT_TICKER_NAME = Coin.upper() + '/' + Pairing.upper()
TRADING_TICKER_NAME = Coin.lower() + Pairing.lower()

INVESTMENT_AMOUNT_DOLLARS = bs.get_account(Pairing.upper())
HOLDING_QUANTITY = bs.get_account(Coin.upper())

API_KEY = key
API_SECRET = secret
exchange = ccxt.binance()
client = Client(API_KEY, API_SECRET)

# FETCH THE DATA
def fetch_data(ticker):
    global exchange
    bars,ticker_df = None, None

    try:
        bars = exchange.fetch_ohlcv(ticker, timeframe=f'{CANDLE_DURATION_IN_MIN}m', limit=100)
    except:
        print(f"Error in fetching data from the exchange for {ticker} pair")

    if bars is not None:
        ticker_df = pd.DataFrame(bars[:-1], columns=['at', 'open', 'high', 'low', 'close', 'vol'])
        ticker_df['Date'] = pd.to_datetime(ticker_df['at'], unit='ms')
        ticker_df['symbol'] = ticker

    return ticker_df


# COMPUTE THE TECHNICAL INDICATORS & APPLY THE TRADING STRATEGY
def RSI_MACD(ticker_df):
    macd_result = 'WAIT'
    final_result = 'WAIT'

    # BUY or SELL based on MACD crossover points and the RSI value at that point
    macd, signal, hist = talib.MACD(ticker_df['close'], fastperiod = 12, slowperiod = 26, signalperiod = 9)
    last_hist = hist.iloc[-1]
    prev_hist = hist.iloc[-2]
    if not np.isnan(prev_hist) and not np.isnan(last_hist):
        # If hist value has changed from negative to positive or vice versa, it indicates a crossover
        macd_crossover = (abs(last_hist + prev_hist)) != (abs(last_hist) + abs(prev_hist))
        if macd_crossover:
            macd_result = 'BUY' if last_hist > 0 else 'SELL'

    if macd_result != 'WAIT':
        rsi = talib.RSI(ticker_df['close'], timeperiod = 14)
        # Consider last 3 RSI values
        last_rsi_values = rsi.iloc[-3:]

        if (float(last_rsi_values.min()) <= float(RSI_OVERSOLD)):
            final_result = 'BUY'
        elif (float(last_rsi_values.max()) >= float(RSI_OVERBOUGHT)):
            final_result = 'SELL'
            
    return final_result
    
def get_trade_recommendation(ticker_df):
    order = []
    #RSI & MACD indicator 
    rsimacd = RSI_MACD(ticker_df)
    if(active_rsi and rsimacd != "WAIT"):
        order.append(rsimacd) 
        print("RSI + MACD : " + rsimacd)
    #bollinger-bands
    bollinger = bb.bollinger_trade_logic()
    if(active_bollinger and bollinger != "WAIT"):
        order.append(bollinger)
        print("Bollinger : " + bollinger)
    #pattern recognition
    interval = str(CANDLE_DURATION_IN_MIN if(CANDLE_DURATION_IN_MIN in [1, 3, 5, 15, 30]) else 1) + "m"
    pattern = pr.patern_recog('1m', "1 day ago", Coin.upper() + Pairing.upper())
    if(active_pattern != '0' and pattern != "WAIT"):
        order.append(pattern)
        print("PATTERN : " + pattern)
    # final choice
    order.sort()
    
    if(len(order)%2 == 1):
        final_result = order[len(order)//2]
    else:
        final_result = "WAIT"
        
    return final_result


# EXECUTE THE TRADE
def execute_trade(trade_rec_type, trading_ticker,value):
    
    price = 0
    global client, HOLDING_QUANTITY
    order_placed = False
    side_value = 'buy' if (trade_rec_type == "BUY") else 'sell'
    try:
        ticker_price_response = client = Client (API_KEY, API_SECRET)
        current_price = bs.get_price(Coin.upper() + Pairing.upper())

        scrip_quantity = value
        print(f"PLACING ORDER {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: "
              f"{trading_ticker}, {side_value}, Price : {current_price}, quantity : {scrip_quantity}, TimeStamp : {int(time.time() * 1000)} ")
        
        if(trade_rec_type == "BUY"):
            bs.buy_coin(value)
            #a =1
        elif(trade_rec_type == "SELL"):
            bs.sell_coin(value)
            #a =1
        print(" ORDER PLACED")
       
        order_placed = True
        
        price = current_price
    except:
        print("\nALERT!!! UNABLE TO COMPLETE ORDER")

    return order_placed, price


