# import the Binance client from python-binance module
from binance.client import Client

# import required library for timing our DCA
from time import time

# define your API key and secret
API_KEY = "my_api_key"
API_SECRET = "my_secret_api"

# define the client
client = Client (API_KEY, API_SECRET)

# CONFIG VARIABLES DEFINED HERE
coin = "BTC"
quantity = 0.0014
pairing = "USDT"
frequency = 1
Squantity = 0.00099

def buy_coin():
    return client.order_market_buy(symbol=coin+pairing,quantity=quantity)

def sell_coin():
    return client.order_market_sell(symbol=coin+pairing,quantity=Squantity)
    
def main():
    print(f"Selling {coin}")
    sell_coin()
    """
  while True:
    print(f"Buying {coin}")
    buy_coin()
    time.sleep(frequency*604800)
    """
    
if __name__ == '__main__':
  main()