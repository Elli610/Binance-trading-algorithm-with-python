import matplotlib.pyplot as plt
import bollingerbandsV3 as bb
import pandas as pd
import numpy as np
from binance.client import Client
from config import *
import sql
import datetime
import time
import sqlite3

def graph_bollinger(interval,starttime):
    client = Client(key, secret)
    symbol = Coin.upper() + Pairing.upper()
    # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    # request historical candle (or klines) data using timestamp from above, interval either every min, hr, day or month
    # starttime = '30 minutes ago UTC' for last 30 mins time
    # e.g. client.get_historical_klines(symbol='ETHUSDTUSDT', '1m', starttime)
    # starttime = '1 Dec, 2017', '1 Jan, 2018'  for last month of 2017
    # e.g. client.get_historical_klines(symbol='BTCUSDT', '1h', "1 Dec, 2017", "1 Jan, 2018")
    #starttime = '1 day ago UTC'  # to start for 1 day ago
    #interval = '1m'
    bars = client.get_historical_klines(symbol, interval, starttime)
    #pprint.pprint(bars)
    
    for line in bars:        # Keep only first 5 columns, "date" "open" "high" "low" "close"
        del line[5:]
    df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close']) #  2 dimensional tabular data
    
    symbol_df = df
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
    df = symbol_df 
    df=df.astype(float)
    df[['close', 'sma','upper', 'lower']].plot()
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Close price',fontsize=18)
    x_axis = df.index
    plt.fill_between(x_axis, df['lower'], df['upper'], color='grey',alpha=0.30)
    plt.scatter(df.index,df['buy'], color='purple',label='Buy',  marker='^', alpha = 1) # purple = buy
    plt.scatter(df.index,df['sell'], color='red',label='Sell',  marker='v', alpha = 1)  # red = sell
    plt.show()
    
# Viewing general statistics
def trade_count(t):
    """
    (t entier)
    return le nombre de trades sur :
    le dernier jour si t = 1, 
    dernière heure si t = 2, 
    dernière semaine si t = 3, 
    dernier mois (30 jours) si t = 4, 
    dernière année (365 jours) si t = 5
    renvoie le dernier jour sinon
    """
    currentTimeStamp = round(time.time())
    dict = {1 : 86400, 2 : 3600, 3 : 604800, 4 : 2592000, 5 : 31536000}
    if (t in dict):
        lastTimeStamp = currentTimeStamp - dict[int(t)]
    else : 
        lastTimeStamp = currentTimeStamp - dict[1]
    #datetime.datetime.fromtimestamp(1657136492242).strftime('%Y-%m-%d %H:%M:%S')
    order = "SELECT Count(*) FROM trade WHERE timestamp > '" + str(lastTimeStamp) + "'"
    conn = sqlite3.connect('Databases/trading_Ledger.db') 
    cursor = conn.cursor()
    cursor.execute(order)
    out = cursor.fetchone()
    conn.close()
    return out[0]

def total_sell(t):
    """
    (t entier)
    return le total acheté sur :
    le dernier jour si t = 1, 
    dernière heure si t = 2, 
    dernière semaine si t = 3, 
    dernier mois (30 jours) si t = 4, 
    dernière année (365 jours) si t = 5
    renvoie le dernier jour sinon
    """
    currentTimeStamp = round(time.time())
    dict = {1 : 86400, 2 : 3600, 3 : 604800, 4 : 2592000, 5 : 31536000}
    if (t in dict):
        lastTimeStamp = currentTimeStamp - dict[int(t)]
    else : 
        lastTimeStamp = t
    #datetime.datetime.fromtimestamp(1657136492242).strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('Databases/trading_Ledger.db')
    
    order = "SELECT Count(*) FROM trade WHERE side == 'SELL' AND timestamp > '" + str(lastTimeStamp) + "'"
    cursor = conn.cursor()
    cursor.execute(order)
    total = cursor.fetchone()
    
    order = "SELECT SUM(price) FROM trade WHERE side == 'SELL' AND timestamp > '" + str(lastTimeStamp) + "'"
    cursor = conn.cursor()
    cursor.execute(order)
    totalValue = cursor.fetchone()
    
    conn.close()
    
    return (total[0],totalValue[0])  

def total_buy(t):
    """
    (t entier)
    return le total acheté sur :
    le dernier jour si t = 1, 
    dernière heure si t = 2, 
    dernière semaine si t = 3, 
    dernier mois (30 jours) si t = 4, 
    dernière année (365 jours) si t = 5
    renvoie le dernier jour sinon
    """
    currentTimeStamp = round(time.time())
    dict = {1 : 86400, 2 : 3600, 3 : 604800, 4 : 2592000, 5 : 31536000}
    if (t in dict):
        lastTimeStamp = currentTimeStamp - dict[int(t)]
    else : 
        lastTimeStamp = t
    #datetime.datetime.fromtimestamp(1657136492242).strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('Databases/trading_Ledger.db')
    
    order = "SELECT Count(*) FROM trade WHERE side == 'BUY' AND timestamp > '" + str(lastTimeStamp) + "'"
    cursor = conn.cursor()
    cursor.execute(order)
    total = cursor.fetchone()
    
    order = "SELECT SUM(price) FROM trade WHERE side == 'BUY' AND timestamp > '" + str(lastTimeStamp) + "'"
    cursor = conn.cursor()
    cursor.execute(order)
    totalValue = cursor.fetchone()
    
    conn.close()
    
    return (total[0],totalValue[0])
    
def pnl(t): # ne marche pas si on fait des échanges en dehors du programme
    """
    (t entier)
    return le pnl sur :
    le dernier jour si t = 1, 
    dernière heure si t = 2, 
    dernière semaine si t = 3, 
    dernier mois (30 jours) si t = 4, 
    dernière année (365 jours) si t = 5
    renvoie le timestamp correspondant à t sinon
    """
    currentTimeStamp = round(time.time())
    dict = {1 : 86400, 2 : 3600, 3 : 604800, 4 : 2592000, 5 : 31536000}
    if (t in dict):
        lastTimeStamp = currentTimeStamp - dict[int(t)]
    else : 
        lastTimeStamp = t
        
    # obtenir la liste des trades depuis t
    conn = sqlite3.connect('Databases/trading_Ledger.db')
    
    order = "SELECT * FROM trade WHERE timestamp > '" + str(lastTimeStamp) + "' ORDER BY timestamp DESC"
    cursor = conn.cursor()
    cursor.execute(order)
    total = cursor.fetchall()
    pnl = 0
    if(len(total) >= 2):
        pnl = total[0][6] - total[-1][6]
    else:
        pnl = 0 
    
    return pnl
    

#afficher les stats
def print_stat():
    # total buy + nb buy
    totBuy = total_buy(1)[1]
    nbBuy = total_buy(1)[0]
    # total sell + nb sell
    totSell = total_sell(1)[1]
    nbSell = total_sell(1)[0]
    # PNL depuis le départ
    pnl = totSell - totBuy
    
    print("")
    print("")
    print('------------------------------------------------------------------------')
    print("")
    print("\t Nombre de Buy au cours des dernières 24 heures : ", nbBuy)
    print("\t Pour une valeur de " + str(totBuy) + " " + Pairing.upper())
    print("")
    print("\t Nombre de Sell au cours des dernières 24 heures : ", nbSell)
    print("\t Pour une valeur de " + str(totSell) + " " + Pairing.upper())
    print("")
    print("\t P&L sur les dernières 24 heures : ", pnl, "*")
    print("")
    print(" * Attention, le p&l n'est pas bon si vous avez échangé sur cette paire sans passer par l'algorithme ! ")
    print("")
    print('------------------------------------------------------------------------')
    print("")
    print("")
    
    