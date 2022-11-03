# import databases
import sql
# import the Binance client from python-binance module
from binance.client import Client
#import config
from config import *
import time 

# define your API key and secret
API_KEY = key
API_SECRET = secret

# define the client
client = Client (API_KEY, API_SECRET)

# CONFIG VARIABLES DEFINED HERE
def get_account(coin):
    info = client.get_account()
    i = info['balances'][0]['asset']
    j = 0
    while ( i != coin.upper()):
        j += 1
        i = info['balances'][j]['asset']        
    return float(info['balances'][j]['free'])

def get_price(paire):
    try:
        a = float(client.get_ticker(symbol=paire)['lastPrice'])
        return a
    except :
        return "ERROR"
    
coin = Coin
initial_quantity_Coin = get_account(Coin.upper())

pairing = Pairing
initial_quantity_Pairing = get_account(Pairing.upper())


def buy_coin(value): 
    client = Client(key, secret)
    info = client.order_market_buy(symbol=coin+pairing,quantity=value)
    if(info['status'] == 'FILLED'):
        sql.addTrade(info["orderId"],
                     info["clientOrderId"], 
                     round(time.time()),
                     info["symbol"],
                     info["side"],
                     info["executedQty"], 
                     info["cummulativeQuoteQty"],
                     "")
        
    timestamp = time.time()
    
    priceCoin = get_price(Coin.upper() + 'USDT') if Coin.upper() != 'USDT' else 1
    coinWallet = Coin.upper() 
    quantityC = get_account(Coin.upper())
    
    sql.addWallet(coinWallet,timestamp,priceCoin,quantityC)
    
    pricePairing = get_price(Pairing.upper() + 'USDT')if Pairing.upper() != 'USDT' else 1
    pairingWallet = get_account(pairing.upper())
    quantityP = get_account(Pairing.upper())
    
    sql.addWallet(pairingWallet,timestamp,pricePairing,quantityP)
    
    return info


def sell_coin(value):
    client = Client(key, secret)
    info = client.order_market_sell(symbol=coin+pairing,quantity=value)
    
    sql.addTrade(info["orderId"],
                 info["clientOrderId"], 
                 round(time.time()),
                 info["symbol"],
                 info["side"],
                 info["executedQty"], 
                 info["cummulativeQuoteQty"],
                 "")
    timestamp = time.time()
    
    priceCoin = get_price(Coin.upper() + 'USDT') if Coin.upper() != 'USDT' else 1
    coinWallet = Coin.upper() 
    quantityC = get_account(Coin.upper())
    
    sql.addWallet(coinWallet,timestamp,priceCoin,quantityC)
    
    pricePairing = get_price(Pairing.upper() + 'USDT')if Pairing.upper() != 'USDT' else 1
    pairingWallet = get_account(pairing.upper())
    quantityP = get_account(Pairing.upper())
    
    sql.addWallet(pairingWallet,timestamp,pricePairing,quantityP)
    return info




"""
    {'symbol': 'BTCUSDT',
     'orderId': 11423623979,
     'orderListId': -1,
     'clientOrderId': 'ZhTtYHf3y5gys0oY2WCjJr',
     'transactTime': 1657136492242,
     'price': '0.00000000',
     'origQty': '0.00053000',
     'executedQty': '0.00053000',
     'cummulativeQuoteQty': '10.80372670',
     'status': 'FILLED',
     'timeInForce': 'GTC',
     'type': 'MARKET',
     'side': 'BUY',
     'fills': [{'price': '20384.39000000',
       'qty': '0.00053000',
       'commission': '0.00003405',
       'commissionAsset': 'BNB',
       'tradeId': 1438281629}]}
"""
