from Oanda import Oanda
from TimeHelper import utc_now
from Environment import env
from Constants import cons
import v20

access_token = env.get(cons.OANDA_TOKEN)
account_id = env.get(cons.OANDA_DEFAULT_ACCOUNT)
domain = env.get(cons.OANDA_TRADE_DOMAIN)

api = v20.Context(domain, 443, token=access_token)

oa = Oanda(api, account_id)

instrument_id = "EUR_USD"
price = round(1.0921, 4)
stop_loss = price - 0.0005
take_profit = price + 0.0005
units = 50
gtdTime = str(utc_now())

oa.place_limit_order(
    instrument_id=instrument_id,
    price=price,
    stop_loss=round(stop_loss, 4),
    take_profit=round(take_profit, 4),
    units=units,
    gtdTime=gtdTime
)
