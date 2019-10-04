from Trader import Trader
from Types import PreOrder
from Constants import trd
from _converter import _converter
from _twilio import _twilio
from asserts import assert_is_not_none, assert_is_none, assert_boolean_true, assert_equal

import pytest
import pandas as pd
import logging


# trader
oar, oac, twilio = Trader.get_dependencies()
trader = Trader(oar, oac, twilio)
logger = logging.getLogger(__name__)


def test_open_trade():
    # trader = Trader()
    # result = trader.open_trade('EURUSD2')
    assert True


def test_calculate_short():
    ask = 1.0010
    bid = 1.0008
    position_size = 500
    take_profit_pips = 0.0007
    stop_loss_pips = 0.0003
    open_price, stop_loss, take_profit, position_size = trader.calculate_short(
        PreOrder(
            instrument="EUR_USD",
            ask=ask,
            bid=bid,
            position_size=position_size,
            position_type=trd.SHORT_TRADE,
            take_profit_pips=take_profit_pips,
            stop_loss_pips=stop_loss_pips,
            time_in_force="GTC")
    )

    open_price = _converter.round4(open_price)
    stop_loss = _converter.round4(stop_loss)
    take_profit = _converter.round4(take_profit)

    logger.debug([open_price, stop_loss, take_profit])

    # open price of short is the bid price.
    assert_equal(open_price, bid)

    # stop loss is based on the ask (1.0010) plus the (0.0003) ie 1.0013
    assert_equal(stop_loss, 1.0013)

    # take profit is based on the bid (1.0008) minus the (0.0007) ie 1.0001
    assert_equal(take_profit, 1.0001)

    # position size should be negative since it is a short.
    assert_equal(position_size, -500)


def test_calculate_long():
    instrument = "EUR_USD"
    ask = 1.0010
    bid = 1.0008
    position_size = 500
    take_profit_pips = 0.0007
    stop_loss_pips = 0.0003
    open_price, stop_loss, take_profit, position_size = trader.calculate_long(
        PreOrder(
            instrument=instrument,
            ask=ask,
            bid=bid,
            position_size=position_size,
            position_type=trd.LONG_TRADE,
            take_profit_pips=take_profit_pips,
            stop_loss_pips=stop_loss_pips,
            time_in_force="GTC")
    )

    open_price = _converter.round4(open_price)
    stop_loss = _converter.round4(stop_loss)
    take_profit = _converter.round4(take_profit)

    logger.debug([open_price, stop_loss, take_profit])

    # open price of long is the ask price.
    assert_equal(open_price, ask)

    # stop loss is based on the bid (1.0010) minus the (0.0003) ie 1.0005
    assert_equal(stop_loss, 1.0005)

    # # take profit is based on the ask (1.0010) plus the (0.0007) ie 1.0017
    assert_equal(take_profit, 1.0017)

    # # position size should be positive since it is a long.
    assert_equal(position_size, 500)
