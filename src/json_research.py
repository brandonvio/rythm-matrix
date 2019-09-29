import json
from Types import Order
from _converter import _converter
from _time import _time


# order = Order(
#     instrument="EUR_USD",
#     position_size=str(-500),
#     open_price=_converter.round4str(1.0011),
#     take_profit=_converter.round5str(1.0012),
#     stop_loss=_converter.round5str(1.0013),
#     fill_type="GTC",
#     time_in_force=(str(_time.utc_now()))
# )

# print(order)
# o = dict(order)


# class Person:
#     first_name = None
#     last_name = None
#     age = None


# b = Person()
# b.first_name = "Brandon"
# b.last_name = "Vicedomini"
# b.age = 45

# x = jsonpickle.encode(b)
# print(x)

orderx = Order(
    instrument="EUR_USD",
    position_size=str(-500),
    open_price=_converter.round4str(1.0011),
    take_profit=_converter.round5str(1.0012),
    stop_loss=_converter.round5str(1.0013),
    fill_type="GTC",
    time_in_force=(str(_time.utc_now()))
)

order_dict = orderx.to_dict()
print(order_dict)

order_dict["position_size"] = -1000

orderx2 = Order.from_dict(order_dict)
print(orderx2)
# orderd = {
#     "instrument": "EUR_USD",
#     "position_size": str(-500),
#     "open_price": _converter.round4str(1.0011),
#     "take_profit": _converter.round5str(1.0012),
#     "stop_loss": _converter.round5str(1.0013),
#     "fill_type": "GTC",
#     "time_in_force": (str(_time.utc_now()))
# }

# print(order)
# print(json.dumps(order))
