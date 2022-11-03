# import the Binance client from python-binance module
from binance.client import Client

# import required library for timing our DCA
from time import time

#import config
from config import *

# define your API key and secret
API_KEY = key
API_SECRET = secret

# define the client
client = Client (API_KEY, API_SECRET)

# CONFIG VARIABLES DEFINED HERE
coin = Coin
initial_quantity_Coin = holding

pairing = Pairing
frequency = 1
initial_quantity_Pairing = initial_investment

def buy_coin(value):
    return client.order_market_buy(symbol=coin+pairing,quantity=value)

def sell_coin(value):
    return client.order_market_sell(symbol=coin+pairing,quantity=value)



"""    
def main():
    print(f"Selling {coin}")
    sell_coin()
  while True:
    print(f"Buying {coin}")
    buy_coin()
    time.sleep(frequency*604800)

if __name__ == '__main__':
  main()
"""