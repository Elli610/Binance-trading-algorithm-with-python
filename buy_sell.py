# import databases
import sql
# import the Binance client from python-binance module
from binance.client import Client
#import config
from config import *

# define your API key and secret
API_KEY = key
API_SECRET = secret

# define the client
client = Client (API_KEY, API_SECRET)

# CONFIG VARIABLES DEFINED HERE
def get_account(coin):
    client = Client(key, secret)
    info = client.get_account()
    i = info['balances'][0]['asset']
    j = 0
    while ( i != coin.upper()):
        j += 1
        i = info['balances'][j]['asset']        
    return float(info['balances'][j]['free'])

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
                     info["transactTime"],
                     info["symbol"],
                     info["side"],
                     info["executedQty"], 
                     info["cummulativeQuoteQty"],
                     "")
    return info


def sell_coin(value):
    client = Client(key, secret)
    info = client.order_market_sell(symbol=coin+pairing,quantity=value)
    
    if(info['status'] == 'FILLED'):
        sql.addTrade(info["orderId"],
                     info["clientOrderId"], 
                     info["transactTime"],
                     info["symbol"],
                     info["side"],
                     info["executedQty"], 
                     info["cummulativeQuoteQty"],
                     "")
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
