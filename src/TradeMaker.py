import pika
import pika.exceptions
import pickle
import collections
import pandas as pd
from Types import Price
from Constants import env
from Constants import trd
from Stategy.DefaultScalp import get_trade
from _rabbit import _rabbit
from _redis import _redis
from _time import _time

rabbit = _rabbit()
redis = _redis()

price_list = []
total_shorts = 0
total_longs = 0
total_notrade = 0
total_spread_too_high = 0


def callback(ch, method, properties, body):
    global total_longs
    global total_shorts
    global total_notrade
    global total_spread_too_high

    t0 = _time.time()
    price = pickle.loads(body)
    print(f"TradeMaker {price.time} {price.ask} {price.bid} {price.mid} {price.spread}")
    price_list.append(price)
    price_list_len = len(price_list)

    if (price_list_len < 500):
        print("Not enough data, no trade.")
        return
    else:
        del price_list[0]

    if price.spread > 1.5:
        total_spread_too_high = total_spread_too_high + 1
        print(f"Spread of {price.spread} is too high, no trade.")
        return

    trade = get_trade(price_list)
    if trade != trd.NO_TRADE:
        print("resetting prepare short/long")
        redis.set_bool(trd.PREPARE_SHORT, False)
        redis.set_bool(trd.PREPARE_LONG, False)

    if trade == trd.NO_TRADE:
        total_notrade = total_notrade + 1

    if trade == trd.LONG_TRADE:
        total_longs = total_longs + 1

    if trade == trd.SHORT_TRADE:
        total_shorts = total_shorts + 1

    t1 = _time.time()
    total_time = t1-t0

    print("trade:", trade)
    print("total_time:", total_time)
    print("total_longs:", total_longs)
    print("total_shorts:", total_shorts)
    print("total_notrade:", total_notrade)
    print("total_spread_too_high:", total_spread_too_high)
    redis.set("total_time", total_time)
    redis.set("total_longs", total_longs)
    redis.set("total_shorts", total_shorts)
    redis.set("total_notrade", total_notrade)
    redis.set("total_spread_too_high", total_spread_too_high)


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
        channel = rabbit.get_oanda_consume_channel(env.OANDA_PRICE_QUEUE_1, callback)
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
    run_mode = redis.get_run_mode()
    redis.set_bool(trd.PREPARE_SHORT, False)
    redis.set_bool(trd.PREPARE_LONG, False)
    redis.set("total_time", 0)
    redis.set("total_longs", 0)
    redis.set("total_shorts", 0)
    redis.set("total_notrade", 0)

    print(f"======={run_mode}=======")
    main(run_mode)
