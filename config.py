import configparser

filename = "config.ini"


config = configparser.ConfigParser()
config.read(filename)

key = config['SETTINGS']['key']
secret = config['SETTINGS']['secret']

Coin = config['SETTINGS']['Coin']
Pairing = config['SETTINGS']['Pairing']

candle_duration = int(config['SETTINGS']['candle_duration']) 

coef_buy = float(config['SETTINGS']['coef_buy'])if (float(config['SETTINGS']['coef_buy']) <= 0.99) else 0.98
coef_sell = float(config['SETTINGS']['coef_sell']) if (float(config['SETTINGS']['coef_sell']) <= 0.99) else 0.98

cryptos = config['SETTINGS']['cryptos'].split(",")

freq_stats = config['SETTINGS']['freq_stats']

#STRATEGY
strategy_simple = True if (config['STRATEGY']["strategy_simple"] == '1') else False
marge = config['STRATEGY']["marge"]
prix_min_vente = config['STRATEGY']["prix_min_vente"]
prix_max_achat = config['STRATEGY']["prix_max_achat"]

#RSI
active_rsi = True if (config['RSI']['active_rsi'] == '1') else False
period = int(config['RSI']['period'])
overbought = int(config['RSI']['overbought'])
oversold = config['RSI']['oversold']


#BOLLINGER BANDS
active_bollinger = True if (config['BOLLINGER BANDS']['active_bollinger'] == '1') else False
interval = str(config['BOLLINGER BANDS']['interval'])
starttime = str(config['BOLLINGER BANDS']['starttime'])


#PATTERN RECOGNITION
active_pattern = config['PATTERN RECOGNITION']['active_pattern'].split(',') if(config['PATTERN RECOGNITION']['active_pattern'] != '0') else '0'
number = int(config['PATTERN RECOGNITION']['number'])
action_buy = int(config['PATTERN RECOGNITION']['action_buy'])
action_sell = int(config['PATTERN RECOGNITION']['action_sell'])

# obtenir infos sur une paire :
"""
def pairingInfo(pair):
    info = Client.get_symbol_info(pair)
    return info
"""
# obtenir infos sur une paire 
#wx_client.send("ticker", { "symbol": 'btcusdt'})

#aide : https://python-binance.readthedocs.io/en/latest/account.html