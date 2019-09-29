from Types import Price
from _time import _time
from asserts import assert_equal
import logging
import pytest

# init.
logger = logging.getLogger(__name__)

# test data.
_instrument = "EUR_USD"
_status = "active"
__time = str(_time.utc_now())
_tradeable = True
_ask = 1.0011
_bid = 1.0010
_mid = 1.00105
_spread = 1.12
_ask_liquidity = 100001
_bid_liquidity = 100002
_ask_closeout = 1
_bid_closeout = 2

_price = Price(instrument=_instrument,
               status=_status,
               time=__time,
               tradeable=_tradeable,
               ask=_ask,
               bid=_bid,
               mid=_mid,
               spread=_spread,
               ask_liquidity=_ask_liquidity,
               bid_liquidity=_bid_liquidity,
               ask_closeout=_ask_closeout,
               bid_closeout=_bid_closeout)


def test_price_instance():
    # validate price object instantiated correctly.
    validate_price(_price)


def test_price_to_from_dict():
    # validate to_dict works correctly.
    price_dict = _price.to_dict()
    assert_equal(type(price_dict), dict)
    validate_price_dict(price_dict)
    price_dict = _price.to_dict()
    dict_price = Price.from_dict(price_dict)
    assert_equal(type(dict_price), Price)
    validate_price(dict_price)


def test_price_from_json():
    # validate
    price_json = _price.to_json()
    assert_equal(type(price_json), str)

    price_bytes = price_json.encode()
    assert_equal(type(price_bytes), bytes)

    json_price = Price.from_json(price_bytes)
    assert_equal(type(json_price), Price)
    validate_price(json_price)


def validate_price_dict(dict):
    assert_equal(_instrument, dict["instrument"])
    assert_equal(_status, dict["status"])
    assert_equal(__time, dict["time"])
    assert_equal(_tradeable, dict["tradeable"])
    assert_equal(_ask, dict["ask"])
    assert_equal(_mid, dict["mid"])
    assert_equal(_spread, dict["spread"])
    assert_equal(_ask_liquidity, dict["ask_liquidity"])
    assert_equal(_bid_liquidity, dict["bid_liquidity"])
    assert_equal(_ask_closeout, dict["ask_closeout"])
    assert_equal(_bid_closeout, dict["bid_closeout"])


def validate_price(price: Price):
    assert_equal(_instrument, price.instrument)
    assert_equal(_status, price.status)
    assert_equal(__time, price.time)
    assert_equal(_tradeable, price.tradeable)
    assert_equal(_ask, price.ask)
    assert_equal(_mid, price.mid)
    assert_equal(_spread, price.spread)
    assert_equal(_ask_liquidity, price.ask_liquidity)
    assert_equal(_bid_liquidity, price.bid_liquidity)
    assert_equal(_ask_closeout, price.ask_closeout)
    assert_equal(_bid_closeout, price.bid_closeout)
