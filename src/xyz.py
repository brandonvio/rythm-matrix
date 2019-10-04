# Candlestick Chart Visualizer
# by NeuralNine Copyright (c) 2019
import datetime as dt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas_datareader as web
from mpl_finance import candlestick_ohlc

# Define start and end date
start = dt.datetime(2010, 1, 1)
end = dt.datetime.now()

# Load data for the specific stock
df = web.DataReader('AAPL', 'yahoo', start, end)

# Reorder the 4 crucial columns
df = df[['Open', 'High', 'Low', 'Close']]

# Reset the index and convert date into float
df.reset_index(inplace=True)
df['Date'] = df['Date'].map(mdates.date2num)

# Define a new subplot
ax = plt.subplot()

# Plot the candlestick chart and put date on x-Axis
candlestick_ohlc(ax, df.values, width=5, colorup='g', colordown='r')
ax.xaxis_date()

# Turn on grid
ax.grid(True)

# Show plot
plt.show()
