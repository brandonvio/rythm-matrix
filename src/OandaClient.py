import sys
import json
import v20
import requests
from _time import _time
from Types import Order
from Environment import get_env
from Constants import env
from ColorPrint import *


class OandaClient:
    def __init__(self, api, account_id):
        self.api = api
        self.account_id = account_id

    def get_account_summary(self):
        response = self.api.account.summary(self.account_id).get("account", 200)
        return response

    def get_account_instruments(self):
        response = self.api.account.instruments(self.account_id).get("instruments", 200)
        return response

    def get_open_positions(self):
        response = self.api.position.list_open(self.account_id).get("positions", 200)
        return response

    def get_pending_orders(self):
        response = self.api.order.list_pending(self.account_id).get("orders", 200)
        return response

    def get_transaction_list(self):
        response = self.api.transaction.list(self.account_id)
        transaction_list = {}
        transaction_list["from"] = response.get("from")
        transaction_list["to"] = response.get("to")
        transaction_list["pageSize"] = response.get("pageSize")
        transaction_list["count"] = response.get("count")
        transaction_list["pages"] = response.get("pages")
        transaction_list["lastTransactionID"] = response.get("lastTransactionID")
        return transaction_list

    def get_transaction_range(self, from_id, to_id, filter):
        response = self.api.transaction.range(
            self.account_id,
            fromID=from_id,
            toID=to_id,
            type=filter).get("transactions", 200)
        return response

    @staticmethod
    def get_dependencies():
        access_token = get_env(env.OANDA_TOKEN)
        oanda_trade_domain = get_env(env.OANDA_TRADE_DOMAIN)
        api = v20.Context(oanda_trade_domain, 443, token=access_token)
        account_id = get_env(env.OANDA_DEFAULT_ACCOUNT)
        return api, account_id


def log(message):
    print(message)


def log_json(message):
    print(message)
