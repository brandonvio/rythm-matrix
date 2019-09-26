import collections
from dateutil import parser

Price = collections.namedtuple(
    "Price",
    [
        "instrument",
        "tradeable",
        "status",
        "time",
        "ask",
        "ask_liquidity",
        "bid",
        "bid_liquidity",
        "ask_closeout",
        "bid_closeout"
    ]
)


def price_from_dict(price_dict):
    _price = Price(
        instrument=price_dict["instrument"],
        status=price_dict["status"],
        time=parser.parse(price_dict["time"]),
        tradeable=bool(price_dict["tradeable"]),
        ask=float(price_dict["asks"][0]["price"]),
        bid=float(price_dict["bids"][0]["price"]),
        ask_liquidity=int(price_dict["asks"][0]["liquidity"]),
        bid_liquidity=int(price_dict["bids"][0]["liquidity"]),
        ask_closeout=float(price_dict["closeoutAsk"]),
        bid_closeout=float(price_dict["closeoutBid"])
    )
    return _price
