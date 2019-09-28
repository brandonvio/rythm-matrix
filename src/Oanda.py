import sys
import json
import v20
import requests
from _time import _time
from Types import Order
from Environment import get_env
from Constants import env
from ColorPrint import *


class Oanda:
    def __init__(self, oanda_trade_domain, access_token, account_id):
        self.oanda_trade_domain = oanda_trade_domain
        self.oanda_token = access_token
        self.account_id = account_id
        self.configure_endpoints()

    def get(self, url):
        token = self.oanda_token
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"An error occurred {resp.status_code} {resp.text}")
            return None
        return resp.json()

    def post(self, url, data):
        token = self.oanda_token
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(url, headers=headers, json=data)
        return resp.status_code, resp.json()

    def configure_endpoints(self):
        domain = self.oanda_trade_domain
        account_id = self.account_id
        self.instruments_endpoint = f'https://{domain}/v3/accounts/{account_id}/instruments'
        self.open_positions_endpoint = f'https://{domain}/v3/accounts/{account_id}/openPositions'
        self.orders_endpoint = f"https://{domain}/v3/accounts/{account_id}/orders"
        self.pricing_endpoint = f"https://{domain}/v3/accounts/{account_id}/pricing"
        self.open_trades_enpoint = f"https://{domain}/v3/accounts/{account_id}/openTrades"
        self.replace_order_endpoint = f"https://{domain}/v3/accounts/{account_id}/orders/[order_id]"

    @staticmethod
    def get_dependencies():
        oanda_trade_domain = get_env(env.OANDA_TRADE_DOMAIN)
        access_token = get_env(env.OANDA_TOKEN)
        account_id = get_env(env.OANDA_DEFAULT_ACCOUNT)
        return oanda_trade_domain, access_token, account_id


def log(message):
    print(message)


def log_json(message):
    print(message)
