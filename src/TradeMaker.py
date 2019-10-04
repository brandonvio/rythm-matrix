import pika
import pika.exceptions
import collections
import pandas as pd
import sys

from Trader import Trader
from Types import Price
from Types import PreOrder
from Constants import env
from Constants import trd
from Stategy.DefaultScalp import get_trade
from _rabbit import _rabbit
from _redis import _redis
from _time import _time

module_name = "TradeMaker"
rabbit = _rabbit()
redis = _redis()

# trader = Trader(*Trader.get_dependencies())
trader = Trader(*Trader.get_dependencies_bt())
price_list = []


def callback(ch, method, properties, body):
    # start timer.
    t0 = _time.time()

    # trading configurables.
    position_size, take_profit_pips, stop_loss_pips, time_in_force = 50, 0.0001, 0.0005, "GTC"

    price = Price.from_json(body)
    print(module_name, price.time, price.instrument, price.ask, price.bid)
    price_list.append(price.to_simple_dict())
    price_list_len = len(price_list)

    if (price_list_len < 500):
        print("Not enough data, no trade.")
        return
    else:
        del price_list[0]

    if price.spread > 1.5:
        redis.incr_one("total_spread_too_high")
        print(f"Spread of {price.spread} is too high, no trade.")
        return

    trade = get_trade(price_list)
    if trade != trd.NO_TRADE:
        print("resetting prepare short/long")
        redis.set_bool(trd.PREPARE_SHORT, False)
        redis.set_bool(trd.PREPARE_LONG, False)
        trader.send_order(
            PreOrder(ask=price.ask,
                     bid=price.bid,
                     instrument=price.instrument,
                     position_type=trade,
                     position_size=position_size,
                     take_profit_pips=take_profit_pips,
                     stop_loss_pips=stop_loss_pips,
                     time_in_force=time_in_force)
        )

    redis.incr_one(trade)

    t1 = _time.time()
    total_time = t1-t0

    print("trade:", trade)
    print("total_time:", total_time)

    # get values from redis
    print("total_longs:", redis.get(trd.LONG_TRADE))
    print("total_shorts:", redis.get(trd.SHORT_TRADE))
    print("total_notrade:", redis.get(trd.NO_TRADE))
    print("total_spread_too_high:", redis.get("total_spread_too_high"))


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
    redis.expire_now("order_log")
    redis.expire_now(trd.LONG_TRADE)
    redis.expire_now(trd.SHORT_TRADE)
    redis.expire_now(trd.NO_TRADE)
    print(f"======={run_mode}=======")
    main(run_mode)
