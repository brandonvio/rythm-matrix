from ColorPrint import *
from _redis import _redis
import jsonpickle

redis = _redis()


class OandaRest:
    def send_limit_order(self, order):
        cprintg(order)
        x = jsonpickle.encode(order)
        redis.rpush("order_log", x)
        return True
