import time
from datetime import datetime
import pandas as pd
import numpy as np
from wazirx_sapi_client.rest import Client
import ccxt
import talib
from config import *
import buy_sell as bs
import sql
import bollingerbands as bb

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
wx_client = Client(api_key=API_KEY, secret_key=API_SECRET)

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
    if(rsimacd != "WAIT"):
        order.append(rsimacd) 
    #bollinger-bands
    bollinger = bb.bollinger_trade_logic()
    if(bollinger != "WAIT"):
        order.append(bollinger)
    
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
    global wx_client, HOLDING_QUANTITY
    order_placed = False
    side_value = 'buy' if (trade_rec_type == "BUY") else 'sell'
    try:
        ticker_price_response = wx_client.send("ticker", { "symbol": trading_ticker})
        if (ticker_price_response[0] in [200, 201]):
            
            current_price = float(ticker_price_response[1]['lastPrice'])

            scrip_quantity = value
            print(f"PLACING ORDER {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: "
                  f"{trading_ticker}, {side_value}, Price : {current_price}, quantity : {scrip_quantity}, TimeStamp : {int(time.time() * 1000)} ")
            
            if(trade_rec_type == "BUY"):
                bs.buy_coin(value)
            elif(trade_rec_type == "SELL"):
                bs.sell_coin(value)
            
            """
            order_response = wx_client.send("create_order",
                                        {"symbol": trading_ticker, "side": side_value, "type": "limit",
                                         "price": current_price, "quantity": scrip_quantity,
                                         "recvWindow": 10000, "timestamp": int(time.time() * 1000)})
            """
            
            print(" ORDER PLACED")
            #HOLDING_QUANTITY = scrip_quantity if trade_rec_type == "BUY" else HOLDING_QUANTITY
           
            order_placed = True
            
            price = current_price
    except:
        print("\nALERT!!! UNABLE TO COMPLETE ORDER")

    return order_placed, price


