import sys
import json
import v20
import requests
from _time import _time
from Types import Order
from Environment import get_env
from Constants import env
from ColorPrint import *
from Oanda import Oanda


class OandaRest(Oanda):
    def __init__(self, oanda_trade_domain, access_token, account_id):
        super().__init__(oanda_trade_domain, access_token, account_id)

    def send_limit_order(self, order: Order):
        order_data = {
            "order": {
                "stopLossOnFill": {
                    "timeInForce": "GTC",
                    "price": order.stop_loss
                },
                "takeProfitOnFill": {
                    "timeInForce": "GTC",
                    "price": order.take_profit
                },
                "clientExtensions": {
                    "ext_1": f"matrix trading {order.instrument}"
                },
                "instrument": order.instrument,
                "units": order.position_size,
                "price": order.open_price,
                "type": "LIMIT",
                "positionFill": "DEFAULT",
                "triggerCondition": "DEFAULT",
                "timeInForce": order.time_in_force  # GTC, FOK
            }
        }

        log_json(order_data)
        status_code, resp = self.post(self.orders_endpoint, order_data)
        log(status_code)
        log(resp)
        print(status_code, resp)

        result = False
        if status_code == 201:
            if resp.has_key("orderFillTransaction"):
                trade_id = resp["orderFillTransaction"]["tradeOpened"]["tradeID"]
                filled_price = resp["orderFillTransaction"]["tradeOpened"]["price"]
                cprintg(f"Order filled for {order.instrument}. TradeID {trade_id}. Filled at {filled_price}.")
                result = True
            elif "orderCreateTransaction" in resp.keys():
                pass
            else:
                pass
        else:
            cprintr("Order failed.")

        return result


def log(message):
    print(message)


def log_json(message):
    print(message)
