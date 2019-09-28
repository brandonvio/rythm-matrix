import pandas as pd
import numpy as np
from finta import TA
from Constants import trd
from _redis import _redis

redis = _redis()
print("init strategy")
trade_log = []


def get_trade(price_dict):
    # init dataframe.
    df = pd.DataFrame(price_dict)
    df = df.set_index('time')
    build_df(df)

    # resample and get atr.
    df_res1 = df['mid'].resample("30s").ohlc()
    print("df_res1 len", len(df_res1))

    atr = get_atr(df_res1, 10)
    if atr < 0.00010:
        print(f"ATR of {atr} is too low. No trade.")
        return trd.NO_TRADE

    print("len(df)", len(df))

    # int trade.
    trade = trd.NO_TRADE
    current_row = df.iloc[-1]

    # get trend direction.
    _trend = get_trend(current_row["ema_trend_up"], current_row["ema_trend_down"])
    if _trend == 0:
        trade_log.append("no trend, no trade.")
        return trd.NO_TRADE  # no trade

    # get current price relative to fast ema (ema_1).
    current_price_to_ema_1 = -1
    if current_row["ask"] > current_row["ema_1"]:
        current_price_to_ema_1 = 1

    # trend is down
    if _trend == -1:
        prepare_short = redis.get_bool(trd.PREPARE_SHORT)
        print("prepare_short:", prepare_short)
        # if price is higher than fast ema, prepare short.
        if current_price_to_ema_1 == 1:
            if not prepare_short:
                redis.set_bool(trd.PREPARE_SHORT, True)
                log(f"{current_row.name}, short prepared.")
        else:
            # if price is lower than emas, check prepare short.
            if prepare_short:
                log(f"{current_row.name}, return short.")
                trade = trd.SHORT_TRADE

    # trend is up
    if _trend == 1:
        prepare_long = redis.get_bool(trd.PREPARE_LONG)
        print("prepare_long:", prepare_long)
        # if price is lower than fast ema, prepare long.
        if current_price_to_ema_1 == -1:
            if not prepare_long:
                redis.set_bool(trd.PREPARE_LONG, True)
                log(f"{current_row.name}, long prepared.")
        else:
            # if price is lower than emas, check prepare long.
            if prepare_long:
                log(f"{current_row.name}, return long.")
                trade = trd.LONG_TRADE

    return (trade)


def build_df(df):
    # df["sma_0"] = pd.Series.rolling(df['mid'], window=400).mean()
    # df["sma_1"] = pd.Series.rolling(df['mid'], window=100).mean()
    # df["sma_2"] = pd.Series.rolling(df['mid'], window=400).mean()
    # df["sma_4"] = pd.Series.rolling(df['mid'], window=500).mean()
    df["ema_0"] = pd.Series.ewm(df['mid'], span=10).mean()
    df["ema_1"] = pd.Series.ewm(df['mid'], span=200).mean()
    df["ema_2"] = pd.Series.ewm(df['mid'], span=300).mean()
    df["ema_3"] = pd.Series.ewm(df['mid'], span=400).mean()
    df.dropna(inplace=True)
    df["ema_trend_up"] = np.where((df['ema_1'] > df['ema_2']) & (df["ema_2"] > df["ema_3"]), True, False)
    df["ema_trend_down"] = np.where((df['ema_1'] < df['ema_2']) & (df["ema_2"] < df["ema_3"]), True, False)


def get_atr(df, interval):
    df["ATR10"] = TA.ATR(df, interval)
    current_row = df.iloc[-1]
    return current_row["ATR10"]
    # df_bid = df['bid'].resample(interval).ohlc()
    # df_resampled = pd.concat([df_ask, df_bid], axis=1, keys=['mid', 'bid'])


def log(message):
    trade_log.append(message)


def get_trend(trend_up, trend_down):
    trend = 0
    if trend_up and not trend_down:
        trend = 1
    elif trend_down and not trend_up:
        trend = -1
    return trend
