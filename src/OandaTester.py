from OandaRest import OandaRest
from OandaClient import OandaClient
from Trader import Trader
from Types import Order, PreOrder
from _time import _time
from _converter import _converter

domain, token, account = OandaRest.get_dependencies()
oar = OandaRest(domain, token, account)

api, account_id = OandaClient.get_dependencies()
oac = OandaClient(api, account_id)

trader = Trader(*Trader.get_dependencies())


def place_order():
    instrument = "EUR_USD"
    price = 1.09315
    stop_loss = price - 0.0005
    take_profit = price + 0.0005
    units = 50
    gtdTime = str(_time.utc_now())

    order = Order(
        instrument=instrument,
        position_size=units,
        open_price=_converter.round5str(price),
        take_profit=_converter.round5str(take_profit),
        stop_loss=_converter.round5str(stop_loss),
        time_in_force="GTC",
        fill_type="GTC"
    )

    oar.send_limit_order(order)


def get_account_info():
    result = oac.get_account_summary()
    print(result)


def get_pending_orders():
    result = oac.get_pending_orders()
    print(type(result))
    print(result)

    for order in result:
        print(order)


def get_open_positions():
    result = oac.get_open_positions()
    print(type(result))
    print(result)


def trader_has_open_positions():
    print("trader_has_open_positions")
    result = trader.has_open_position("EUR_USD")
    print(result)


def trader_has_pending_orders():
    print("trader_has_pending_orders")
    result = trader.has_pending_order("EUR_USD")
    print(result)


def trader_send_order():

    position_size, take_profit_pips, stop_loss_pips, time_in_force = 50, 0.0001, 0.0005, "GTC"
    instrument, ask, bid = "EUR_USD", 1.09393, 1.09381

    pre_order = PreOrder(ask=ask,
                         bid=bid,
                         instrument=instrument,
                         position_type="LONG_TRADE",
                         position_size=position_size,
                         take_profit_pips=take_profit_pips,
                         stop_loss_pips=stop_loss_pips,
                         time_in_force=time_in_force)

    trader.send_order(pre_order)


if __name__ == "__main__":
    # get_account_info()
    # get_open_positions()
    # trader_has_open_positions()
    # place_order()
    # get_pending_orders()
    # trader_has_pending_orders()
    # trader_has_open_positions()
    trader_send_order()
