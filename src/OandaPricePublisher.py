import pika
import pickle
import collections
import time
from Types import Price, price_from_dict
from Constants import cons
from Environment import env
from OandaStream import OandaStream
from RabbitHelper2 import RabbitHelper
from RedisHelper import redis_helper
from MongoHelper import get_data_from_oanda_stream

rabbit_helper = RabbitHelper()
oanda_stream = OandaStream()


def mongodb_loop():
    records = get_data_from_oanda_stream(2000)
    # publish to queue
    for i, record in enumerate(records):
        # time.sleep(1)
        publish_price(record)


def publish_price(price_dict):
    _price = price_from_dict(price_dict)
    print(_price.time, _price.instrument, _price.ask, _price.bid)
    _price = pickle.dumps(_price)
    rabbit_helper.publish_oanda_price(_price)


def main(run_mode):
    # redis_helper.set_run_mode_live()
    rabbit_helper.configure_oanda_publish_channel()
    if run_mode == cons.RUN_MODE_LIVE:
        print('oanda_stream')
        oanda_stream.stream(publish_price)
    else:
        print('mongodb_loop')
        mongodb_loop()


if __name__ == "__main__":
    redis_helper.set_run_mode_testing()
    run_mode = redis_helper.get_run_mode()
    print(f"======={run_mode}=======")
    main(run_mode)
