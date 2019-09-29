import pika
import sys
from Types import Price
from Constants import env
from Environment import get_env
from OandaStream import OandaStream
from _rabbit import _rabbit
from _redis import _redis
from _mongo import _mongo
from _time import _time

module_name = "OandaPricePublisher"
rabbit = _rabbit()
redis = _redis()
mongo = _mongo()
oanda_stream = OandaStream()


def mongodb_loop():
    records = mongo.get_data_from_oanda_stream(4000)
    # publish to queue
    for i, record in enumerate(records):
        # time.sleep(1)
        publish_price(record)


def publish_price(price_dict):
    price = Price.from_origin(price_dict)
    print(module_name, price.time, price.instrument, price.ask, price.bid)
    price = price.to_json()
    rabbit.publish_oanda_price(price)


def main(run_mode):
    # redis_.set_run_mode_live()
    rabbit.configure_oanda_publish_channel()
    if run_mode == env.RUN_MODE_LIVE:
        print('oanda_stream')
        oanda_stream.stream(publish_price)
    else:
        print('mongodb_loop')
        mongodb_loop()


if __name__ == "__main__":
    redis.set_run_mode_testing()
    run_mode = redis.get_run_mode()
    print(f"======={run_mode}=======")
    main(run_mode)
