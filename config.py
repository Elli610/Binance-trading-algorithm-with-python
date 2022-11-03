import configparser

filename = "config.ini"


config = configparser.ConfigParser()
config.read(filename)

key = config['SETTINGS']['key']
secret = config['SETTINGS']['secret']

Coin = config['SETTINGS']['Coin']
Pairing = config['SETTINGS']['Pairing']

initial_investment = float(config['SETTINGS']['initial_investment']) # quantité pairing
holding = float(config['SETTINGS']['holding']) # quantité coin

candle_duration = int(config['SETTINGS']['candle_duration']) #en minutes

#RSI
period = int(config['RSI']['period'])
overbought = int(config['RSI']['overbought'])
oversold = config['RSI']['oversold']


# obtenir infos sur une paire :
"""
def pairingInfo(pair):
    info = Client.get_symbol_info(pair)
    return info
"""
# obtenir infos sur une paire 
#wx_client.send("ticker", { "symbol": 'btcusdt'})
