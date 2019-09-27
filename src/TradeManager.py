import pika
import pickle
import collections
import pandas as pd
from Types import Price
from Constants import env
from RedisHelper import redis_
from MongoHelper import get_testing_price_data
from RabbitHelper2 import RabbitHelper
from Stategy.DefaultScalp import get_trade

price_list = []
rabbit_helper = RabbitHelper()


def callback(ch, method, properties, body):
    global price_list
    price = pickle.loads(body)
    print(f"TradeManager {price.ask} {price.bid}")


def main(run_mode):
    global price_list
    if run_mode == env.RUN_MODE_TESTING:
        price_list = get_testing_price_data()
        print(len(price_list))
    else:
        price_list = []

    channel = rabbit_helper.get_oanda_consume_channel(env.OANDA_PRICE_QUEUE_2, callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    run_mode = redis_.get_run_mode()
    print(f"======={run_mode}=======")
    main(run_mode)
