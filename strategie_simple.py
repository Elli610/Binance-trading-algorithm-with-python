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
import main_Algo as ma

def mainss(ticker_data,currently_holding,current_balance): #savoir si on veut une base avec usdt ou avec btc 
    price = bs.get_price(Coin.upper() + Pairing.upper())
    paire = Coin.upper() + Pairing.upper()
    if(float(current_balance) > float(currently_holding * price)):
        while (float(current_balance) > float(currently_holding * price)):
            if(price > prix_min_vente):
                if(ma.canITrade(paire,current_balance * 0.98 ,trade_rec_type,price)):
                    sell_coin(current_balance * 0.98)
                else : 
                    print(" Unable to place order")
            else : 
                time.sleep(55.0)    
    
    while (float(current_balance) < float(currently_holding * price)):
        #suit les indicatuers pour obtenir un bon point d'entrée
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
        
    
    # Maintenant on commence 
    


    