import os
from binance.client import Client # needs pip install python-binance
import pprint
import pandas as pd     
import numpy as np
import matplotlib.pyplot as plt   
from config import *
import time
api_key = key     
api_secret = secret  
client = Client(api_key, api_secret)
symbol = Coin.upper() + Pairing.upper()


def get_data_frame():
    bars = client.get_historical_klines(symbol, "1m", starttime)
    #pprint.pprint(bars)
    
    for line in bars:        # Keep only first 5 columns, "date" "open" "high" "low" "close"
        del line[5:]
    df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close']) #  2 dimensional tabular data
    return df

    
def buy_or_sell(df):
    buy  = pd.to_numeric(df['buy'], downcast='float')[-1]
    sell = pd.to_numeric(df['sell'], downcast='float')[-1]
    
    # get current price of the symbol
    current_price = client.get_symbol_ticker(symbol =symbol)
    
    # get current price of the symbol
    current_price = client.get_symbol_ticker(symbol =symbol)
    if float(current_price['price']) >= sell:  # sell order
        return("SELL")
        #print("sell sell sell...")
        #sell_order = client.order_market_sell(symbol=symbol, quantity=0.01)
        #print(sell_order)
    elif float(current_price['price']) <= buy:  # buy order
        return("BUY")
        #print("RECOMMENDATION FROM bollinger-bands : BUY")
        #buy_order = client.order_market_buy(symbol=symbol, quantity=0.001)
        #print(buy_order)
            
    return "WAIT"
    
            
def bollinger_trade_logic():
    symbol_df = get_data_frame()
    period = 20
    # small time Moving average. calculate 20 moving average using Pandas over close price
    symbol_df['sma'] = symbol_df['close'].rolling(period).mean()
    # Get standard deviation
    symbol_df['std'] = symbol_df['close'].rolling(period).std()
    # Calculate Upper Bollinger band
    symbol_df['upper'] = symbol_df['sma']  + (2 * symbol_df['std'])
    # Calculate Lower Bollinger band
    symbol_df['lower'] = symbol_df['sma']  - (2 * symbol_df['std'])
    # To print in human readable date and time (from timestamp)
    symbol_df.set_index('date', inplace=True)
    symbol_df.index = pd.to_datetime(symbol_df.index, unit='ms') # index set to first column = date_and_time
 
    # prepare buy and sell signals. The lists prepared are still panda dataframes with float nos
    close_list = pd.to_numeric(symbol_df['close'], downcast='float')
    upper_list = pd.to_numeric(symbol_df['upper'], downcast='float')
    lower_list = pd.to_numeric(symbol_df['lower'], downcast='float')
    symbol_df['buy'] = np.where(close_list < lower_list,   symbol_df['close'], np.NaN )
    symbol_df['sell'] = np.where(close_list > upper_list,   symbol_df['close'], np.NaN )
    with open('bollinger.txt', 'w') as f:
        f.write(
                symbol_df.to_string()
               )
    
    #plot_graph(symbol_df)
    return buy_or_sell(symbol_df)
