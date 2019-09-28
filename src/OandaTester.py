from OandaRest import OandaRest
from OandaClient import OandaClient
from Types import Order
from _time import _time
from _converter import _converter

domain, token, account = OandaRest.get_dependencies()
oar = OandaRest(domain, token, account)

api, account_id = OandaClient.get_dependencies()
oac = OandaClient(api, account_id)


def place_order():
    instrument = "EUR_USD"
    price = round(1.0921, 4)
    stop_loss = price - 0.0005
    take_profit = price + 0.0005
    units = 50
    gtdTime = str(_time.utc_now())

    order = Order(
        instrument=instrument,
        position_size=units,
        open_price=_converter.round4str(price),
        take_profit=_converter.round5str(take_profit),
        stop_loss=_converter.round5str(stop_loss),
        time_in_force="GTC"
    )

    oar.send_limit_order(order)


def get_account_info():
    result = oac.get_account_summary()
    print(result)


def get_open_positions():
    result = oac.get_open_positions()
    print(type(result))
    print(result)


if __name__ == "__main__":
    get_account_info()
    get_open_positions()
    # place_order()
