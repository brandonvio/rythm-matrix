from Oanda import Oanda
from Trader import Trader
import v20
import os
import pytest
import logging
from dotenv import load_dotenv
from asserts import assert_is_not_none, assert_is_none

load_dotenv()
access_token = os.getenv('OANDA_TOKEN')
account_id = os.getenv('OANDA_DEFAULT_ACCOUNT')
api = v20.Context('api-fxtrade.oanda.com', 443, token=access_token)

assert_is_not_none(access_token)
assert_is_not_none(account_id)

oa = Oanda(api, account_id)
logger = logging.getLogger(__name__)
# logger.critical('eggs critical')


def test_get_account_summary():
    resp = oa.get_account_summary()
    # logger.info(resp)
    assert_is_not_none(resp)


def test_get_account_instruments():
    resp = oa.get_account_instruments()
    # logger.info(resp)
    assert_is_not_none(resp)


def test_get_transation_list():
    resp = oa.get_transaction_list()
    # logger.info(resp)
    assert_is_not_none(resp)


def test_get_transaction_range():
    resp = oa.get_transaction_range(1, 1002, None)
    # logger.info(len(resp))
    # for t in resp:
    #     logger.info(t)
    # logger.info(list(resp))
    assert_is_not_none(resp)
