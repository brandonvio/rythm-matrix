import pika
import pickle
import json
import collections
import requests
import time
from RedisHelper import redis_helper
from dateutil import parser
from bson.json_util import dumps
from pymongo import MongoClient
from MongoHelper import get_data_from_oanda_stream
from types import SimpleNamespace as Namespace
from Types import Price, price_from_dict
from Constants import cons
from Environment import env
from RabbitHelper2 import RabbitHelper

rabbit_helper = RabbitHelper()


def mongodb_loop():
    records = get_data_from_oanda_stream(10)
    # publish to queue
    for i, record in enumerate(records):
        time.sleep(1)
        publish_price(record)


def oanda_stream():
    accountID = env.get(cons.OANDA_DEFAULT_ACCOUNT)
    token = env.get(cons.OANDA_TOKEN)
    headers = {"Authorization": f"Bearer {token}"}
    instruments = ["EUR_USD", "USD_JPY", "AUD_USD", "USD_CAD", "USD_CHF", "USD_JPY", "EUR_JPY", "GBP_USD"]
    instrument_url = ""
    for instrument in instruments:
        instrument_url = instrument_url + f"{instrument}%2C"

    stream_domain = env.get(cons.OANDA_STREAM_DOMAIN)
    the_url = f"https://{stream_domain}/v3/accounts/{accountID}/pricing/stream?instruments={instrument_url}"
    r = requests.get(the_url, stream=True, headers=headers)

    print(">>>> Pricing service online! <<<<<")
    for line in r.iter_lines():
        if line:
            line = json.loads(line.decode('utf-8'))
            if line["type"] == "PRICE" and line["instrument"] == "EUR_USD":
                publish_price(line)


def publish_price(price_dict):
    _price = price_from_dict(price_dict)
    print(_price.time, _price.instrument, _price.bid, _price.ask)
    _price = pickle.dumps(_price)
    rabbit_helper.publish_oanda_price(_price)


def main(run_mode):
    if run_mode == cons.RUN_MODE_LIVE:
        print('oanda_stream')
        oanda_stream()
    else:
        print('mongodb_loop')
        mongodb_loop()


if __name__ == "__main__":
    redis_helper.set_run_mode_live()
    run_mode = redis_helper.get_run_mode()
    print(f"======={run_mode}=======")
    main(run_mode)
