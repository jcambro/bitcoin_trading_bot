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

    * Change api for testing
        ** client.API_URL = 'https://testnet.binance.vision/api'
'''

import os
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import pandas as pd


TRADING_FEE_PERCENT = 0.0750

# intialize dataframe to hold bitcoin price data along with an error flag
btc_price = {'BTCUSDT': pd.DataFrame(columns=['date', 'price']), 'error':False}

# logic uses a state machine of either 'buy' or 'sell' depending on if bitcoin
# is owned already. Default to buy (assume no bitcoin ownership)
BUY_STATE = True


def btc_trade_history(msg):
    ''' define how to process incoming WebSocket messages '''
    if msg['e'] != 'error':
        print(msg['c'])
        # place the incoming price at the end of the dataframe with the current timestamp
        btc_price['BTCUSDT'].loc[len(btc_price['BTCUSDT'])] = [pd.Timestamp.now(), float(msg['c'])]
        btc_price['error'] = False
    else:
        btc_price['error'] = True


def main():
    # Retrieve the api keys from Windows Environmental Variables
    api_key = os.environ.get('binance_api')
    api_secret = os.environ.get('binance_secret')

    # Intiate the client
    client = Client(api_key, api_secret)

    # start a websocket that will automatically call our btc_trade_history
    # method and update our btc_price dictionary with up-to-date information
    bsm = BinanceSocketManager(client)
    conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', btc_trade_history)
    bsm.start()

    # see bitcoin balance
    # print(client.get_asset_balance(asset='BTC'))

    while len(btc_price['BTCUSDT']) == 0:
        # wait for Websocket to recieve first data point
        sleep(0.1)

    # Wait for dataframe to populate for 5 min
    sleep(300)

    # TODO change to a while True loop later. For testing limit the amount
    # of loops
    x = 0
    while x < 10:
        # Error check the websocket
        if btc_price['error']:
            # restart socket
            bsm.stop_socket(conn_key)
            bsm.start()
            btc_price['error'] = False
        else:
            # TODO logic for buying or selling
            x += 1

        sleep(0.1)

    # stop & terminate websocket
    bsm.stop_socket(conn_key)
    reactor.stop()


if __name__ == '__main__':
    main()
