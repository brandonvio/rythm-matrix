import json
from abc import ABC
from abc import abstractmethod
from _time import _time


class BaseType(ABC):
    def to_json(self):
        dict = self.to_dict()
        return json.dumps(dict)

    @abstractmethod
    def to_dict(self):
        pass

    def __str__(self):
        return self.to_json()

    @classmethod
    def from_json(cls, body):
        dict = json.loads(body)
        return cls.from_dict(dict)

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)


class Price(BaseType):
    def __init__(self, **kwargs):
        self.instrument = kwargs["instrument"]
        self.tradeable = kwargs["tradeable"]
        self.status = kwargs["status"]
        self.time = kwargs["time"]
        self.ask = kwargs["ask"]
        self.ask_liquidity = kwargs["ask_liquidity"]
        self.bid = kwargs["bid"]
        self.bid_liquidity = kwargs["bid_liquidity"]
        self.mid = kwargs["mid"]
        self.ask_closeout = kwargs["ask_closeout"]
        self.bid_closeout = kwargs["bid_closeout"]
        self.spread = kwargs["spread"]

    def to_simple_dict(self):
        return {
            "time": _time.datetime_parse(self.time),
            "ask": self.ask,
            "bid": self.bid,
            "mid": self.mid,
            "spread": self.spread
        }

    def to_dict(self):
        return {
            "instrument": self.instrument,
            "tradeable": self.tradeable,
            "status": self.status,
            "time": self.time,
            "ask": self.ask,
            "ask_liquidity": self.ask_liquidity,
            "bid": self.bid,
            "bid_liquidity": self.bid_liquidity,
            "mid": self.mid,
            "ask_closeout": self.ask_closeout,
            "bid_closeout": self.bid_closeout,
            "spread": self.spread
        }

    @staticmethod
    def from_origin(price_dict):
        ask = float(price_dict["asks"][0]["price"])
        bid = float(price_dict["bids"][0]["price"])
        mid = round(((ask + bid) / 2), 5)
        spread = round((ask - bid) * 10000, 2)
        return Price(instrument=price_dict["instrument"],
                     status=price_dict["status"],
                     time=str(price_dict["time"]),
                     tradeable=bool(price_dict["tradeable"]),
                     ask=ask,
                     bid=bid,
                     mid=mid,
                     spread=spread,
                     ask_liquidity=int(price_dict["asks"][0]["liquidity"]),
                     bid_liquidity=int(price_dict["bids"][0]["liquidity"]),
                     ask_closeout=float(price_dict["closeoutAsk"]),
                     bid_closeout=float(price_dict["closeoutBid"]))


class Order(BaseType):
    def __init__(self, **kwargs):
        self.instrument = kwargs["instrument"]
        self.position_size = kwargs["position_size"]
        self.open_price = kwargs["open_price"]
        self.take_profit = kwargs["take_profit"]
        self.stop_loss = kwargs["stop_loss"]
        self.time_in_force = kwargs["time_in_force"]

    def to_dict(self):
        return {
            "instrument": self.instrument,
            "position_size": self.position_size,
            "open_price": self.open_price,
            "take_profit": self.take_profit,
            "stop_loss": self.stop_loss,
            "time_in_force": self.time_in_force
        }


class PreOrder(BaseType):
    def __init__(self, **kwargs):
        self.ask = kwargs["ask"]
        self.bid = kwargs["bid"]
        self.instrument = kwargs["instrument"]
        self.position_type = kwargs["position_type"]
        self.position_size = kwargs["position_size"]
        self.take_profit_pips = kwargs["take_profit_pips"]
        self.stop_loss_pips = kwargs["stop_loss_pips"]
        self.time_in_force = kwargs["time_in_force"]

    def to_dict(self):
        return {
            "ask": self.ask,
            "bid": self.bid,
            "instrument": self.instrument,
            "position_type": self.position_type,
            "position_size": self.position_size,
            "take_profit_pips": self.take_profit_pips,
            "stop_loss_pips": self.stop_loss_pips,
            "time_in_force": self.time_in_force
        }
