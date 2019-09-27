"""
This file proviides an example of how to use plotly to produce
an ohlc candlestick chart.
"""
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from MongoHelper import get_testing_price_data


def resample(df, interval):
    df_resampled = df['ask'].resample(interval).ohlc()
    # df_bid = df['bid'].resample(interval).ohlc()
    # df_resampled = pd.concat([df_ask, df_bid], axis=1, keys=['ask', 'bid'])
    df_resampled.fillna(method='ffill', inplace=True)
    print(df_resampled.tail())
    print("interval", interval, "len", len(df_resampled.index))
    return df_resampled


price_data = get_testing_price_data()
df = pd.DataFrame(price_data)
df = df.set_index('time')
dfh = resample(df, '5T')


fig = go.Figure(data=[go.Candlestick(x=dfh.index,
                                     open=dfh['open'],
                                     high=dfh['high'],
                                     low=dfh['low'],
                                     close=dfh['close'])])

fig.show()
