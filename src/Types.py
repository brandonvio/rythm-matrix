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
        "mid",
        "ask_closeout",
        "bid_closeout",
        "spread"
    ]
)

Order = collections.namedtuple(
    "Order",
    [
        "instrument",
        "position_size",
        "open_price",
        "take_profit",
        "stop_loss",
        "time_in_force"
    ]
)

PreOrder = collections.namedtuple(
    "PreOrder",
    [
        "ask",
        "bid",
        "instrument",
        "position_type",
        "position_size",
        "take_profit_pips",
        "stop_loss_pips",
        "fill_type"
    ]
)


def price_from_dict(price_dict):
    ask = float(price_dict["asks"][0]["price"])
    bid = float(price_dict["bids"][0]["price"])
    mid = round(((ask + bid) / 2), 5)
    spread = round((ask - bid) * 10000, 2)

    _price = Price(
        instrument=price_dict["instrument"],
        status=price_dict["status"],
        time=parser.parse(price_dict["time"]),
        tradeable=bool(price_dict["tradeable"]),
        ask=ask,
        bid=bid,
        mid=mid,
        spread=spread,
        ask_liquidity=int(price_dict["asks"][0]["liquidity"]),
        bid_liquidity=int(price_dict["bids"][0]["liquidity"]),
        ask_closeout=float(price_dict["closeoutAsk"]),
        bid_closeout=float(price_dict["closeoutBid"])
    )
    return _price
