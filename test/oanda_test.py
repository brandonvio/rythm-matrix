from OandaRest import OandaRest
from OandaClient import OandaClient
import pytest
import logging
from asserts import assert_is_not_none, assert_is_none


logger = logging.getLogger(__name__)
# logger.critical('eggs critical')

domain, token, account = OandaRest.get_dependencies()
oar = OandaRest(domain, token, account)

api, account_id = OandaClient.get_dependencies()
oac = OandaClient(api, account_id)


def test_get_account_summary():
    resp = oac.get_account_summary()
    # logger.info(resp)
    assert_is_not_none(resp)


def test_get_account_instruments():
    resp = oac.get_account_instruments()
    # logger.info(resp)
    assert_is_not_none(resp)


def test_get_transation_list():
    resp = oac.get_transaction_list()
    # logger.info(resp)
    assert_is_not_none(resp)


def test_get_transaction_range():
    resp = oac.get_transaction_range(1, 1002, None)
    # logger.info(len(resp))
    # for t in resp:
    #     logger.info(t)
    # logger.info(list(resp))
    assert_is_not_none(resp)
