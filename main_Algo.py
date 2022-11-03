import strategie as s
import time
from datetime import datetime
import pandas as pd
import numpy as np
from binance.client import Client
import ccxt
#import talib
from config import *
import buy_sell as bs
import trade_statistics as stat
import strategie_simple


# Initialize Variables
CANDLE_DURATION_IN_MIN = candle_duration

RSI_PERIOD = period
RSI_OVERBOUGHT = overbought
RSI_OVERSOLD = oversold

CCXT_TICKER_NAME = Coin.upper() + '/' + Pairing.upper()
TRADING_TICKER_NAME = Coin.lower() + Pairing.lower()
paire = Coin.upper() + Pairing.upper()

INVESTMENT_AMOUNT_DOLLARS = bs.get_account(Pairing.upper())
HOLDING_QUANTITY = bs.get_account(Coin.upper())

API_KEY = key
API_SECRET = secret
exchange = ccxt.binance()
client = Client (API_KEY, API_SECRET)

def canITrade(paire,value,trade_rec_type,price):
    out = True
    price = float(price)
    if(trade_rec_type != 'BUY' and trade_rec_type != "SELL"):
        out = False 
    try :
        if(bs.get_price(paire) == 'ERROR'):
            out = False
    except :
        pass
    if(value > bs.get_account(Coin.lower()) and trade_rec_type == "SELL" and value * price < 10.02):
        #print("a")
        out = False
    if(value > bs.get_account(Pairing.lower())/price and trade_rec_type == "BUY" and value * price < 10.01):
        out = False
    if(trade_rec_type == 'BUY' and (value * price < 10.01)):
        out = False
    if(trade_rec_type == 'SELL' and (value * price < 10.01)):
        out = False
    #print(" Can i trade ? ",out)
    return out

def initialisation():
    print('\f')
    print('\n------------------------------------------------------------------------\n')
    print(" \t \t \t INITIALISATION \n ")
    print("\t Vous traidez sur la paire", Coin.upper()+Pairing.upper() + "\n")
    print("\t Durée des bougies",CANDLE_DURATION_IN_MIN,"minute")
    print("\t Fréquence d'affichage des statistiques :",freq_stats, "minutes \n")
    print("\t\t Statut des indicateurs : \n")
    print("\t RSI/MACD :", active_rsi)
    print("\t Bollinger Bands :", active_bollinger)
    if( active_pattern == '0'):
        print("\t Reconnaissance des paternes : Désactivé")
    else:
        print("\t Reconnaissance des paternes : \n")
        for i in active_pattern :
            print(" \t     - ",i)
    if(active_pattern == '0' and active_rsi == False and active_bollinger == False):
        print('\t\t ATTENTION !!!')
        print('\t\t Tous les indicateurs sont désactivés, aucun trade ne sera effectué')
    print('\n------------------------------------------------------------------------\n')

def main():
    # print initialisation
    
    initialisation()
    timer = round(time.time())
    
    ccxt_ticker = CCXT_TICKER_NAME
    trading_ticker = TRADING_TICKER_NAME

    currently_holding = HOLDING_QUANTITY
    current_balance = INVESTMENT_AMOUNT_DOLLARS
    i = 1
    while 1:
        # FETCH THE DATA
        ticker_data = s.fetch_data(ccxt_ticker)
        
        if ticker_data is not None:
            if(strategy_simple):
                strategie_simple.mainss(ticker_data,currently_holding,current_balance)
            else:           
                    # COMPUTE THE TECHNICAL INDICATORS & APPLY THE TRADING STRATEGY
                    trade_rec_type = s.get_trade_recommendation(ticker_data)
                    #trade_rec_type == "BUY"
                    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}  TRADING RECOMMENDATION: {trade_rec_type}')#' FROM {indic}')
           
                    # EXECUTE THE TRADE
                    
                    if (trade_rec_type == 'BUY' ) or (trade_rec_type == 'SELL'):
                        
                        price = bs.get_price(Coin.upper() + Pairing.upper())
                        
                        # value calculation
                        value = round(coef_buy*float(current_balance)/price,5) if(trade_rec_type == 'BUY') else round(coef_sell*float(currently_holding),5)#round(float(current_balance) / price ,5)
                        trade_successful = False
                        #print("value = ",value)
                        #print("price = ",price)
                        #print(canITrade(paire,value,trade_rec_type,price))
                        if(canITrade(paire,value,trade_rec_type,price)):
                            print(f'Placing {trade_rec_type} order')
                            trade_successful,price = s.execute_trade(trade_rec_type,trading_ticker,value)
                            if(trade_successful != True):
                                print(f'Unable to place {trade_rec_type} order')
                                
                        
                    print(" " + Coin.upper() + " balance = " + str(currently_holding))
                    print(" " + Pairing.upper() + " balance = " + str(current_balance)) 
                    print("")
                        
                    time.sleep(CANDLE_DURATION_IN_MIN*55)
                
        else:
            
            print(f'Unable to fetch ticker data {ccxt_ticker}. Retrying in 5 seconds...')
            time.sleep(5)
        currently_holding = bs.get_account(Coin)
        current_balance = bs.get_account(Pairing)
        
        
        # Print stats
        
        if(round(time.time()) - timer >= i * int(freq_stats) * 60):
            stat.print_stat()
            i += 1


       