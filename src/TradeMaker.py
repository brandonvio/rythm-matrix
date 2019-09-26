import pika
import pickle
import collections
import pandas as pd
from Types import Price
from Constants import cons
from RedisHelper import redis_helper
from MongoHelper import get_testing_price_data
from RabbitHelper2 import RabbitHelper
from Stategy.DefaultScalp import get_trade

price_list = []
rabbit_helper = RabbitHelper()


def callback(ch, method, properties, body):
    global price_list
    price = pickle.loads(body)
    print(f"TradeMaker {price.ask} {price.bid}")
    price_list.append(price)
    df = pd.DataFrame(price_list)
    df = df.set_index('time')
    # print(df.tail())
    # print(len(df))
    df_t = {}
    df_t['tick'] = df
    df_t['5S'] = resample(df, '5S')
    df_t['30S'] = resample(df, '30S')
    df_t['1T'] = resample(df, '1T')
    df_t['5T'] = resample(df, '5T')
    df_t['1H'] = resample(df, '1H')
    trade = get_trade(df_t)
    print("trade:", trade)


def resample(df, interval):
    df_resampled = df['ask'].resample(interval).ohlc()
    # df_bid = df['bid'].resample(interval).ohlc()
    # df_resampled = pd.concat([df_ask, df_bid], axis=1, keys=['ask', 'bid'])
    df_resampled.fillna(method='ffill', inplace=True)
    # print(df_resampled.tail())
    # print("interval", interval, "len", len(df_resampled.index))
    return df_resampled


def main(run_mode):
    global price_list
    if run_mode == cons.RUN_MODE_TESTING:
        price_list = get_testing_price_data()
        print(len(price_list))
    else:
        price_list = []

    channel = rabbit_helper.get_oanda_consume_channel(cons.OANDA_PRICE_QUEUE_1, callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    run_mode = redis_helper.get_run_mode()
    print("=======", run_mode, "=======")
    main(run_mode)
