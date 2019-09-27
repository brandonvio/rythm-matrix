import v20
from Oanda import Oanda
from Environment import get_env
from Constants import env
from _time import _time


access_token = get_env(env.OANDA_TOKEN)
account_id = get_env(env.OANDA_DEFAULT_ACCOUNT)
domain = get_env(env.OANDA_TRADE_DOMAIN)

api = v20.Context(domain, 443, token=access_token)
oa = Oanda(api, account_id)

instrument_id = "EUR_USD"
price = round(1.0921, 4)
stop_loss = price - 0.0005
take_profit = price + 0.0005
units = 50
gtdTime = str(_time.utc_now)

oa.place_limit_order(
    instrument_id=instrument_id,
    price=price,
    stop_loss=round(stop_loss, 4),
    take_profit=round(take_profit, 4),
    units=units,
    gtdTime=gtdTime
)
