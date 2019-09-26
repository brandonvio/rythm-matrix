from finta import TA


def get_trade(data):
    # df_t['5S'] = resample(df, '5S')
    # df_t['30S'] = resample(df, '30S')
    # df_t['1T'] = resample(df, '1T')
    # df_t['5T'] = resample(df, '5T')
    # df_t['1H'] = resample(df, '1H')
    # trade = get_trade(df_t)
    # print(data)
    dfh = data['1H']

    row_1 = dfh.iloc[-1]

    print("get_trade", row_1[row_1.index])
    return 0


def configure_ema_trend(df, ema1, ema2, ema3):
    df["ema_1"] = TA.EMA(df, 5)
    df["ema_2"] = TA.EMA(df, 10)
    df["ema_3"] = TA.EMA(df, 20)

    df["trend_up"] = df["ema_1"] > df["ema_2"] > df["ema_3"]
    df["trend_down"] = df["ema_1"] < df["ema_2"] < df["ema_3"]
    # TA.M
