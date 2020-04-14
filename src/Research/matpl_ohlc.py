################################################################################################
#	name:	timeseries_OHLC_with_SMA.py
#	desc:	creates OHLC graph with overlay of simple moving averages
#	date:	2018-06-15
#	Author:	conquistadorjd
################################################################################################
import pandas as pd
# import pandas_datareader as datareader
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
# from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from get_test_data import get_test_data

print('*** Program Started ***')

df = get_test_data("2T")

# Converting date to pandas datetime format
# df['date'] = pd.to_datetime(df.index)
df['date'] = df['date'].apply(mdates.date2num)

# Creating required data in new DataFrame OHLC
ohlc = df[['date', 'open', 'high', 'low', 'close']].copy()
# In case you want to check for shorter timespan
# ohlc =ohlc.tail(60)
ohlc['SMA50'] = ohlc["close"].rolling(50).mean()


f1, ax = plt.subplots(figsize=(10, 5))

# plot the candlesticks
candlestick_ohlc(ax, ohlc.values, width=.001, colorup='green', colordown='red')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Creating SMA columns
ohlc['SMA5'] = ohlc['close'].rolling(5).mean()
ohlc['SMA10'] = ohlc['close'].rolling(10).mean()
ohlc['SMA20'] = ohlc['close'].rolling(20).mean()
ohlc['SMA50'] = ohlc['close'].rolling(50).mean()
ohlc['SMA100'] = ohlc['close'].rolling(100).mean()
ohlc['SMA200'] = ohlc['close'].rolling(200).mean()

# Plotting SMA columns
ax.plot(ohlc['date'], ohlc['SMA5'], color='blue', label='SMA5')
ax.plot(ohlc['date'], ohlc['SMA10'], color='blue', label='SMA10')
ax.plot(ohlc['date'], ohlc['SMA20'], color='blue', label='SMA20')
ax.plot(ohlc['date'], ohlc['SMA50'], color='green', label='SMA50')
ax.plot(ohlc['date'], ohlc['SMA100'], color='blue', label='SMA100')
ax.plot(ohlc['date'], ohlc['SMA200'], color='blue', label='SMA200')

# Saving image
# plt.savefig('OHLC with SMA HDFC.png')

# In case you dont want to save image but just displya it

# ohlc.to_csv('ohlc.csv')
plt.show()
# print('*** Program ended ***')
