import sys
import json
import v20
import requests
from Environment import get_env
from Constants import env
from ColorPrint import *


class Oanda:
    def __init__(self, api, accountID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accountID = accountID
        self.oanda_trade_domain = get_env(env.OANDA_TRADE_DOMAIN)
        self.oanda_token = get_env(env.OANDA_TOKEN)
        self.api = api
        self.configure_endpoints()

    def get_account_summary(self):
        response = self.api.account.summary(self.accountID).get("account", 200)
        return response

    def get_account_instruments(self):
        response = self.api.account.instruments(self.accountID).get("instruments", 200)
        return response

    def get_transaction_list(self):
        response = self.api.transaction.list(self.accountID)
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
            self.accountID,
            fromID=from_id,
            toID=to_id,
            type=filter)
        transactions = response.get("transactions", 200)
        return transactions

    def send_limit_order(self, instrument_id, price, stop_loss, take_profit, units, gtdTime):
        # TODO: Remove take profit, return better data.
        stop_loss = str(stop_loss)
        take_profit = str(take_profit)
        units = str(units)
        price = str(round(price, 4))
        orders_endpoint = self.orders_endpoint
        order_data = {
            "order": {
                "stopLossOnFill": {
                    "timeInForce": "GTC",
                    "price": stop_loss
                },
                "takeProfitOnFill": {
                    "timeInForce": "GTC",
                    "price": take_profit
                },
                "clientExtensions": {
                    "ext_1": f"matrix trading {instrument_id}"
                },
                "instrument": instrument_id,
                "units": units,
                "price": price,
                "type": "LIMIT",
                "positionFill": "DEFAULT",
                "triggerCondition": "DEFAULT",
                "timeInForce": "GTC",
                "gtdTime": str(gtdTime)
            }
        }
        log_json(order_data)
        status_code, resp = self.post(orders_endpoint, order_data)
        log(status_code)
        log(resp)

        result = False
        if status_code == 201:
            if "orderFillTransaction" in resp.keys():
                trade_id = resp["orderFillTransaction"]["tradeOpened"]["tradeID"]
                filled_price = resp["orderFillTransaction"]["tradeOpened"]["price"]
                cprintg(f"Order filled for {instrument_id}. TradeID {trade_id}. Filled at {filled_price}.")
                result = True
            elif "orderCreateTransaction" in resp.keys():
                cprintg(resp["orderCreateTransaction"])
            else:
                cprintg(resp)
        else:
            cprintr("Order failed.")

        return result

    def post(self, _url, _data):
        token = self.oanda_token
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(_url, headers=headers, json=_data)
        return resp.status_code, resp.json()

    def configure_endpoints(self):
        domain = self.oanda_trade_domain
        accountID = self.accountID
        self.instruments_endpoint = f'https://{domain}/v3/accounts/{accountID}/instruments'
        self.open_positions_endpoint = f'https://{domain}/v3/accounts/{accountID}/openPositions'
        self.orders_endpoint = f"https://{domain}/v3/accounts/{accountID}/orders"
        self.pricing_endpoint = f"https://{domain}/v3/accounts/{accountID}/pricing"
        self.open_trades_enpoint = f"https://{domain}/v3/accounts/{accountID}/openTrades"
        self.replace_order_endpoint = f"https://{domain}/v3/accounts/{accountID}/orders/[order_id]"


def log(message):
    print(message)


def log_json(message):
    print(message)
