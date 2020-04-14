"""
This file proviides an example of how to use plotly to produce
an ohlc candlestick chart.
"""
import plotly.graph_objects as go
import pandas as pd
from get_test_data import get_test_data


df = get_test_data('60T')

fig = go.Figure(data=[go.Candlestick(x=df.index,
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close'])])

fig.show()
