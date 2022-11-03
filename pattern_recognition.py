from config import * 
import talib
import strategie as s
from binance.client import Client
#from datetime import date
import pandas as pd


stockticker = Coin.upper() + Pairing.upper()

def get_df(interval,starttime,symbol):
    client = Client(key, secret)
    # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    # request historical candle (or klines) data using timestamp from above, interval either every min, hr, day or month
    # starttime = '30 minutes ago UTC' for last 30 mins time
    # e.g. client.get_historical_klines(symbol='ETHUSDTUSDT', '1m', starttime)
    # starttime = '1 Dec, 2017', '1 Jan, 2018'  for last month of 2017
    # e.g. client.get_historical_klines(symbol='BTCUSDT', '1h', "1 Dec, 2017", "1 Jan, 2018")
    #starttime = '1 hour ago UTC'  # to start for 1 day ago
    #interval = '1m'
    bars = client.get_historical_klines(symbol, interval, starttime)
    #pprint.pprint(bars)
    
    for line in bars:        # Keep only first 5 columns, "date" "open" "high" "low" "close"
        del line[5:]
    df = pd.DataFrame(bars, columns=['date', 'Open', 'High', 'Low', 'Close']) #  2 dimensional tabular data
    return df

def patern_recog(interval, starttime, symbol):
    dataframe = get_df(interval, starttime, symbol)

    open = dataframe['Open']
    high = dataframe['High']
    low = dataframe['Low']
    close = dataframe['Close']
    #dataframe = dataframe[len(dataframe)-5 : ]
    threeLineStrike = talib.CDL3LINESTRIKE(open,high,low,close)
    threeBlackCrow = talib.CDL3BLACKCROWS(open,high,low,close)
    eveningStar = talib.CDLEVENINGSTAR(open,high,low,close)
    engulfing = talib.CDLENGULFING(open,high,low,close)
    dragonflyDoji = talib.CDLDRAGONFLYDOJI(open,high,low,close)
    gravestoneDoji = talib.CDLGRAVESTONEDOJI(open,high,low,close)
    tasukigap = talib.CDLTASUKIGAP(open,high,low,close)
    hammer = talib.CDLHAMMER(open,high,low,close)
    darkCloudCover = talib.CDLDARKCLOUDCOVER(open,high,low,close)
    piercingLine = talib.CDLPIERCING(open,high,low,close)
    
    for i in active_pattern : 
        if( i == '3 Line Strike') : 
            dataframe['3 Line Strike'] = threeLineStrike
        elif(i == '3 Black Crow'):
            dataframe['3 Black Crow'] = threeBlackCrow
        elif(i == 'Evening Star'):
            dataframe['Evening Star'] = eveningStar
        elif(i == 'Engulfing'):
            dataframe['Engulfing'] = engulfing
        elif(i == 'Dragonfly Doji'):
            dataframe['Dragonfly Doji'] = dragonflyDoji
        elif(i == 'Gravestone Doji'):
            dataframe['Gravestone Doji'] = gravestoneDoji
        elif(i == 'Tasuki Gap'):
            dataframe['Tasuki Gap'] = tasukigap
        elif(i == 'Hammer'):
            dataframe['Hammer'] = hammer
        elif(i == 'DarkCloudCover'):
            dataframe['DarkCloudCover'] = darkCloudCover
        elif(i == 'Piercing Line'):
            dataframe['Piercing Line'] = piercingLine


    #topCandles = ["3 Line Strike","3 Black Crow","Evening Star","Engulfing","Dragonfly Doji","Gravestone Doji","Tasuki Gap","Hammer","DarkCloudCover","Piercing Line"]

    dataframe['result'] = 0
    
    for x in dataframe.index:
        for cd in active_pattern:
            if dataframe.loc[x, cd] == -100:
                #dataframe.loc[x, cd] = "Bearish"
                dataframe.loc[x, 'result'] -= 1
            if dataframe.loc[x, cd] == 100:
                #dataframe.loc[x, cd] = "Bullish"
                dataframe.loc[x, 'result'] += 1
    try :             
        dataframe.drop('Open', axis=1, inplace=True)
    except :
        pass
    try :
        dataframe.drop('High', axis=1, inplace=True)
    except :
        pass
    try :
        dataframe.drop('Low', axis=1, inplace=True)
    except :
        pass
    try : 
        dataframe.drop('Close', axis=1, inplace=True)
    except :
        pass
    try:
        dataframe.drop('3 Line Strike', axis=1, inplace=True)
    except :
        pass
    try :
        dataframe.drop('3 Black Crow', axis=1, inplace=True)
    except :
        pass
    try:
        dataframe.drop('Evening Star', axis=1, inplace=True)
    except :
        pass
    try:
        dataframe.drop('Engulfing', axis=1, inplace=True)
    except :
        pass
    try:
        dataframe.drop('Dragonfly Doji', axis=1, inplace=True)
    except :
        pass
    try:
        dataframe.drop('Gravestone Doji', axis=1, inplace=True)
    except :
        pass
    try:
        dataframe.drop('Tasuki Gap', axis=1, inplace=True)
    except :
        pass
    try:
        dataframe.drop('Hammer', axis=1, inplace=True)
    except :
        pass
    try:
        dataframe.drop('DarkCloudCover', axis=1, inplace=True)
    except :
        pass
    try:
        dataframe.drop('Piercing Line', axis=1, inplace=True)
    except :
        pass
    
    #dataframe.to_csv("dataf.csv")
    dataframe = dataframe[len(dataframe)-number : ]
    if(dataframe['result'].sum() > action_buy):
        return "BUY"
    elif(dataframe['result'].sum() < action_sell):
        return "SELL"
    else:
        return "WAIT"









"""

Data = s.fetch_data('BTC/USDT')
true_high = max(Data['high'][len(Data['high'])-2], Data['high'][len(Data['high'])-1])
true_low = min(Data['low'][len(Data['low'])-2], Data['low'][len(Data['low'])-1])

def TD_differential(Data, true_low, true_high):
    buy = []
    sell = []
    Data.insert("true_low")
    for i in range(len(Data)):
        
        # True low
        Data[i, true_low] = min(Data[i, 2], Data[i - 1, 3])
        Data[i, true_low] = Data[i, 3] - Data[i, true_low]
            
        # True high  
        Data[i, true_high] = max(Data[i, 1], Data[i - 1, 3])
        Data[i, true_high] = Data[i, 3] - Data[i, true_high]
        
        # TD Differential
        if Data[i, 3] < Data[i - 1, 3] and Data[i - 1, 3] < Data[i - 2, 3] and \
           Data[i, true_low] > Data[i - 1, true_low] and Data[i, true_high] < Data[i - 1, true_high]: 
               buy.append(1)
        if Data[i, 3] > Data[i - 1, 3] and Data[i - 1, 3] > Data[i - 2, 3] and \
           Data[i, true_low] < Data[i - 1, true_low] and Data[i, true_high] > Data[i - 1, true_high]: 
               sell.append(1)
    return Data

"""