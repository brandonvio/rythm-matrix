from _mongo import _mongo
from _redis import _redis
from Types import Price
import pandas as pd


def get_test_data(interval):
    mongo = _mongo()
    redis = _redis()
    # redis.lpush('testing_date')
    # price_data = redis.get_list('testing_data')
    # print(len(price_data))
    # if len(price_data) == 0:
    #     price_data = mongo.get_testing_price_data()
    #     price_data = list(map(lambda p: Price.from_origin(p).to_dict(), price_data))
    #     [redis.lpush('testing_data', Price.from_dict(p).to_json()) for p in price_data]
    # else:
    #     price_data = map(lambda p: Price.from_json(p).to_dict(), price_data)

    price_data = mongo.get_testing_price_data()
    price_data = list(map(lambda p: Price.from_origin(p).to_dict(), price_data))

    print(price_data[0])
    df = pd.DataFrame(price_data)
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    df_resampled = df['ask'].resample(interval).ohlc()
    df_resampled['date'] = df_resampled.index.to_series()
    df_resampled['volume'] = 0
    # df_bid = df['bid'].resample(interval).ohlc()
    # df_resampled = pd.concat([df_ask, df_bid], axis=1, keys=['ask', 'bid'])
    df_resampled.fillna(method='ffill', inplace=True)
    # print(df_resampled.tail())
    df_resampled = df_resampled.reset_index(drop=True)
    # del df_resampled['time']
    # x = df_resampled[['date', 'open', 'high', 'low', 'close', 'volume']]
    print("interval", interval, "len", len(df_resampled))
    return df_resampled
