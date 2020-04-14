import pika
import sys
import json
from Types import Price
from Constants import env
from Constants import trd
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


def mongodb_loop(start_date, end_date, record_count):
    records = mongo.get_data_from_oanda_stream(
        start_date=start_date,
        end_date=end_date,
        record_count=record_count)

    # publish to queue
    for _, record in enumerate(records):
        # time.sleep(1)
        publish_price(record)


def publish_price(price_dict):
    price = Price.from_origin(price_dict)
    print(module_name, price.time, price.instrument, price.ask, price.bid)
    price = price.to_json()
    rabbit.publish_oanda_price(price)


def begin_publish_price_data(run_mode, start_date, end_date, record_count):
    # redis_.set_run_mode_live()
    rabbit.configure_oanda_publish_channel()
    if run_mode == env.RUN_MODE_LIVE:
        print('oanda_stream')
        try:
            oanda_stream.stream(publish_price)
        except:
            main(run_mode)
    else:
        print('mongodb_loop')
        mongodb_loop(start_date, end_date, record_count)


def callback(ch, method, properties, body):
    print(body)
    start_params = json.loads(body)
    run_mode = start_params["runMode"]
    start_date = start_params["startDate"]
    end_date = start_params["endDate"]
    record_count = start_params["recordCount"]
    redis.set(env.RUN_MODE, run_mode)
    begin_publish_price_data(run_mode, start_date, end_date, record_count)


def main(run_mode):
    channel = rabbit.get_oanda_consume_channel(env.START_TRADER, callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    redis.set_run_mode_testing()
    run_mode = redis.get_run_mode()
    print(f"======={module_name}=======")
    print(f"======={run_mode}=======")
    main(run_mode)
