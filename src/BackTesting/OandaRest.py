from ColorPrint import *
from Types import Order
from _redis import _redis

redis = _redis()


class OandaRest:
    def send_limit_order(self, order: Order):
        cprintg(order)
        redis.rpush("order_log", order.to_json())
        return True
