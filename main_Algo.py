import strategie as s
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


def canITrade(paire,value,trade_rec_type,price):
    out = True
    if(trade_rec_type != 'BUY' and trade_rec_type != "SELL"):
        return False
    try :
        if(wx_client.send("ticker", { "symbol": paire })[1]['message'] == 'symbol does not have a valid value'):
            return False
    except :
        pass
    if(value > bs.get_account(Coin.lower()) and trade_rec_type == "SELL" and value * price > 10.02):
        #print("a")
        return False
    if(value > bs.get_account(Pairing.lower())/price and trade_rec_type == "BUY" and value > 10):
        return False
    if(trade_rec_type == 'BUY' and (value * float(wx_client.send("ticker", { "symbol": paire })[1]['lastPrice']) < 10.1)):
        return False
    if(trade_rec_type == 'SELL' and (value * float(wx_client.send("ticker", { "symbol": paire })[1]['lastPrice']) < 10.1)):
        return False
    #print(" Can i trade ? ",out)
    return out


def main():
    ccxt_ticker = CCXT_TICKER_NAME
    trading_ticker = TRADING_TICKER_NAME

    currently_holding = HOLDING_QUANTITY
    current_balance = INVESTMENT_AMOUNT_DOLLARS
    
    while 1:
        # FETCH THE DATA
        ticker_data = s.fetch_data(ccxt_ticker)
        
        if ticker_data is not None:
            # COMPUTE THE TECHNICAL INDICATORS & APPLY THE TRADING STRATEGY
            trade_rec_type = s.get_trade_recommendation(ticker_data)
            #trade_rec_type == "BUY"
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}  TRADING RECOMMENDATION: {trade_rec_type}')#' FROM {indic}')
   
            # EXECUTE THE TRADE
            
            if (trade_rec_type == 'BUY' ) or (trade_rec_type == 'SELL'):
                
                print(f'Placing {trade_rec_type} order')
                
                price = float(wx_client.send("ticker", { "symbol": trading_ticker })[1]['lastPrice'])
                
                # New balances 
                value = round(0.9*float(current_balance)/price,5) if(trade_rec_type == 'BUY') else round(0.9*float(currently_holding),5)#round(float(current_balance) / price ,5)
                trade_successful = False
                #print("value = ",value)
                if(canITrade(trading_ticker,value,trade_rec_type,price)):
                    trade_successful,price = s.execute_trade(trade_rec_type,trading_ticker,value)
                else:
                    print(f'Unable to place {trade_rec_type} order')
        
                
            print(" " + Coin.upper() + " balance = " + str(currently_holding))
            print(" " + Pairing.upper() + " balance = " + str(current_balance))    
                
            time.sleep(CANDLE_DURATION_IN_MIN*55)
            
        else:
            
            print(f'Unable to fetch ticker data {ccxt_ticker}. Retrying in 5 seconds...')
            time.sleep(5)
        currently_holding = bs.get_account(Coin)
        current_balance = bs.get_account(Pairing)
        