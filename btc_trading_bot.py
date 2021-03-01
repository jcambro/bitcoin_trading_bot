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


def main():
    # Retrieve the api keys from Windows Environmental Variables
    api_key = os.environ.get('binance_api')
    api_secret = os.environ.get('binance_secret')

    # Intiate the client
    client = Client(api_key, api_secret)

    # Manually change api endpoint for testing
    client.API_URL = 'https://testnet.binance.vision/api'


if __name__ == '__main__':
    main()
