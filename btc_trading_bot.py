'''
John Ambrose 3-1-2021

BITCOIN TRADING BOT

Inspiration and direction from:
    * https://blog.usejournal.com/a-step-by-step-guide-to-building-a-trading-bot-in-any-programming-language-d202ffe91569
    * https://algotrading101.com/learn/binance-python-api-guide/

USING BINANCE AND API
    * pip install python-binance
    * Set the api keys to enviornment variables
        ** 'set binance_api=api_key_here'
        ** 'set binance_secret=api_secret_here'
'''

import os
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor


def btc_trade_history(msg):
    ''' define how to process incoming WebSocket messages '''
    if msg['e'] != 'error':
        print(msg['c'])
        btc_price['close'] = msg['c']   # current days closing price
        btc_price['bid'] = msg['b']     # best bid price
        btc_price['ask'] = msg['a']     # best ask price
    else:
        btc_price['error'] = True


def main():
    # Retrieve the api keys from Windows Environmental Variables
    api_key = os.environ.get('binance_api')
    api_secret = os.environ.get('binance_secret')

    # Intiate the client
    client = Client(api_key, api_secret)
    btc_price = {'error': False}

    # Manually change api endpoint for testing
    client.API_URL = 'https://testnet.binance.vision/api'

    # start a websocket that will automatically call our btc_trade_history
    # method and update our btc_price dictionary with up-to-date information
    bsm = BinanceSocketManager(client)
    conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', btc_trade_history)
    bsm.start()

    # see bitcoin balance
    print(client.get_asset_balance(asset='BTC'))

    # stop & terminate websocket
    bsm.stop_socket(conn_key)
    reactor.stop()


if __name__ == '__main__':
    main()
