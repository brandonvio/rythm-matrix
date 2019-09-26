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
from RabbitHelper import get_rabbit_publish_channel_for_oanda_prices, get_rabbit_connection


def mongodb_loop(channel):
    records = get_data_from_oanda_stream(10)
    # publish to queue
    for i, record in enumerate(records):
        time.sleep(1)
        publish_price(channel, record)


def oanda_stream(channel):
    accountID = env.get(cons.OANDA_DEFAULT_ACCOUNT)
    token = env.get(cons.OANDA_TOKEN)
    headers = {"Authorization": f"Bearer {token}"}
    instruments = ["EUR_USD", "AUD_USD", "USD_CAD", "USD_CHF", "USD_JPY", "EUR_JPY", "GBP_USD"]
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
                publish_price(channel, line)


def publish_price(channel, price_dict):
    _price = price_from_dict(price_dict)
    print(_price.time, _price.instrument, _price.bid, _price.ask)
    message = pickle.dumps(_price)
    channel.basic_publish(exchange='oanda_prices',
                          routing_key='',
                          body=message)


def main(run_mode):
    # connection = get_rabbitmq_connection()
    # channel = get_rabbitmq_channel(connection)
    connection = get_rabbit_connection()
    channel = get_rabbit_publish_channel_for_oanda_prices(connection)

    if run_mode == cons.RUN_MODE_LIVE:
        print('oanda_stream')
        oanda_stream(channel)
    else:
        print('mongodb_loop')
        mongodb_loop(channel)

    connection.close()


if __name__ == "__main__":
    redis_helper.set_run_mode_testing()
    run_mode = redis_helper.get_run_mode()
    print(f"======={run_mode}=======")
    main(run_mode)
