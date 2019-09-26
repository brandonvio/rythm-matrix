from finta import TA
from RedisHelper import redis_helper
import pandas as pd
import numpy as np

print("init strategy")
trade_log = []


def get_trade(price_dict):

    df = pd.DataFrame(price_dict)
    df = df.set_index('time')
    build_df(df)

    print("len(df)", len(df))
    # int function
    trade = 0
    current_row = df.iloc[-1]

    # get trend direction
    _trend = get_trend(current_row["ema_trend_up"], current_row["ema_trend_down"])
    if _trend == 0:
        trade_log.append("no trend, no trade.")
        return 0  # no trade

    # get current price relative to fast ema (ema_1).
    current_price_to_ema_1 = -1
    if current_row["ask"] > current_row["ema_1"]:
        current_price_to_ema_1 = 1

    # trend is down
    if _trend == -1:
        prepare_short = redis_helper.get_bool("prepare_short")
        print("prepare_short:", prepare_short)
        # if price is higher than fast ema, prepare short.
        if current_price_to_ema_1 == 1:
            if not prepare_short:
                redis_helper.set_bool("prepare_short", True)
                log(f"{current_row.name}, short prepared.")
        else:
            # if price is lower than emas, check prepare short, if true, return -1 for short trade.
            if prepare_short:
                log(f"{current_row.name}, return short.")
                trade = -1

    # trend is up
    if _trend == 1:
        prepare_long = redis_helper.get_bool("prepare_long")
        print("prepare_long:", prepare_long)
        # if price is lower than fast ema, prepare long.
        if current_price_to_ema_1 == -1:
            if not prepare_long:
                redis_helper.set_bool("prepare_long", True)
                log(f"{current_row.name}, long prepared.")
        else:
            # if price is lower than emas, check prepare long, if true, return 1 for long trade.
            if prepare_long:
                log(f"{current_row.name}, return long.")
                trade = 1

    return (trade)


def build_df(df):
    # df["sma_0"] = pd.Series.rolling(df['ask'], window=400).mean()
    # df["sma_1"] = pd.Series.rolling(df['ask'], window=100).mean()
    # df["sma_2"] = pd.Series.rolling(df['ask'], window=400).mean()
    # df["sma_4"] = pd.Series.rolling(df['ask'], window=500).mean()
    df["ema_0"] = pd.Series.ewm(df['ask'], span=10).mean()
    df["ema_1"] = pd.Series.ewm(df['ask'], span=200).mean()
    df["ema_2"] = pd.Series.ewm(df['ask'], span=300).mean()
    df["ema_3"] = pd.Series.ewm(df['ask'], span=400).mean()
    df.dropna(inplace=True)
    df["ema_trend_up"] = np.where((df['ema_1'] > df['ema_2']) & (df["ema_2"] > df["ema_3"]), True, False)
    df["ema_trend_down"] = np.where((df['ema_1'] < df['ema_2']) & (df["ema_2"] < df["ema_3"]), True, False)


def log(message):
    trade_log.append(message)


def get_trend(trend_up, trend_down):
    trend = 0
    if trend_up and not trend_down:
        trend = 1
    elif trend_down and not trend_up:
        trend = -1
    return trend
