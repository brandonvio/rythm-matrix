import pika
import pika.exceptions
import pickle
import collections
import pandas as pd
from Types import Price
from Constants import cons
from RedisHelper import redis_helper
from MongoHelper import get_testing_price_data
from RabbitHelper2 import RabbitHelper
from Stategy.DefaultScalp import get_trade
import time


price_list = []
rabbit_helper = RabbitHelper()
total_shorts = 0
total_longs = 0
total_notrade = 0


def callback(ch, method, properties, body):
    global total_longs
    global total_shorts
    global total_notrade

    t0 = time.time()
    price = pickle.loads(body)
    print(f"TradeMaker {price.time} {price.ask} {price.bid}")
    price_list.append(price)
    price_list_len = len(price_list)

    if (price_list_len < 500):
        print("Not enough data, no trade.")
        return
    else:
        del price_list[0]

    trade = get_trade(price_list)
    if trade != 0:
        print("resetting prepare short/long")
        redis_helper.set_bool("prepare_short", False)
        redis_helper.set_bool("prepare_long", False)

    if trade == 0:
        total_notrade = total_notrade + 1

    if trade == 1:
        total_longs = total_longs + 1

    if trade == -1:
        total_shorts = total_shorts + 1

    t1 = time.time()
    total_time = t1-t0
    # trade = 0
    print("trade:", trade)
    print("total_time:", total_time)
    print("total_longs:", total_longs)
    print("total_shorts:", total_shorts)
    print("total_notrade:", total_notrade)
    redis_helper.set("total_time", total_time)
    redis_helper.set("total_longs", total_longs)
    redis_helper.set("total_shorts", total_shorts)
    redis_helper.set("total_notrade", total_notrade)


def resample(df, interval):
    df_resampled = df['ask'].resample(interval).ohlc()
    # df_bid = df['bid'].resample(interval).ohlc()
    # df_resampled = pd.concat([df_ask, df_bid], axis=1, keys=['ask', 'bid'])
    df_resampled.fillna(method='ffill', inplace=True)
    # print(df_resampled.tail())
    # print("interval", interval, "len", len(df_resampled.index))
    return df_resampled


def main(run_mode):
    try:
        channel = rabbit_helper.get_oanda_consume_channel(cons.OANDA_PRICE_QUEUE_1, callback)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except pika.exceptions.StreamLostError:
        print("A StreamErrorException occurred. Continuing.")
        main(run_mode)
    except pika.exceptions.ConnectionWrongStateError:
        print("A ConnectionWrongStateError occurred. Continuing.")
        main(run_mode)


if __name__ == "__main__":
    price_list = []
    run_mode = redis_helper.get_run_mode()
    redis_helper.set_bool("prepare_short", False)
    redis_helper.set_bool("prepare_long", False)
    redis_helper.set("total_time", 0)
    redis_helper.set("total_longs", 0)
    redis_helper.set("total_shorts", 0)
    redis_helper.set("total_notrade", 0)

    print(f"======={run_mode}=======")
    main(run_mode)
