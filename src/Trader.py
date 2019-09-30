from ColorPrint import *
from Types import Order
from Types import PreOrder
from Constants import trd
from OandaClient import OandaClient
from OandaRest import OandaRest
from _twilio import _twilio
from _time import _time
from _converter import _converter

# backtesting
from BackTesting.OandaClient import OandaClient as OandaClientBT
from BackTesting.OandaRest import OandaRest as OandaRestBT
from BackTesting._twilio import _twilio as _twilioBT
# domain, token, account = OandaRest.get_dependencies()


class Trader:
    def __init__(self, oanda_rest: OandaRest, oanda_client: OandaClient, twilio: _twilio):
        self.oanda_rest = oanda_rest
        self.oanda_client = oanda_client
        self.twilio = twilio

    def calculate_long(self, pre_order: PreOrder):
        open_price = pre_order.ask
        take_profit = pre_order.ask + pre_order.take_profit_pips
        stop_loss = pre_order.bid - pre_order.stop_loss_pips
        position_size = pre_order.position_size
        return open_price, stop_loss, take_profit, position_size

    def calculate_short(self, pre_order: PreOrder):
        open_price = pre_order.bid
        take_profit = pre_order.bid + (pre_order.take_profit_pips * -1)
        stop_loss = pre_order.ask - (pre_order.stop_loss_pips * -1)
        position_size = pre_order.position_size * -1
        return open_price, stop_loss, take_profit, position_size

    def send_order(self, pre_order: PreOrder):
        if self.has_open_position(pre_order.instrument):
            log(f"Position already open for {pre_order.instrument}. No trade.")
            return False

        if self.has_pending_order(pre_order.instrument):
            log(f"Order pending for {pre_order.instrument}. No trade.")
            return False

        # Calculate order if long or short.
        if pre_order.position_type == trd.LONG_TRADE:
            open_price, stop_loss, take_profit, position_size = self.calculate_long(pre_order)
        else:
            open_price, stop_loss, take_profit, position_size = self.calculate_short(pre_order)

        order = Order(
            instrument=pre_order.instrument,
            position_size=str(position_size),
            open_price=_converter.round5str(open_price),
            take_profit=_converter.round5str(take_profit),
            stop_loss=_converter.round5str(stop_loss),
            time_in_force=pre_order.time_in_force
        )

        # Send order to Oanda server.
        result = self.oanda_rest.send_limit_order(order)

        # Process result.
        if result:
            message = f"Success. Market order placed for {pre_order.instrument} with stop loss of {stop_loss} and take profit of {take_profit}."
            self.twilio.send_message(message)
        else:
            message = f"Failure. Market order failed for {pre_order.instrument} with stop loss of {stop_loss} and take profit of {take_profit}."
            self.twilio.send_message(message)
        return True

    def has_pending_order(self, instrument):
        pending_order = False

        # get openn positions from api.
        orders = self.oanda_client.get_pending_orders()
        # Check to see if position is already open for this instrument.
        for order in orders:
            if order.instrument == instrument:
                pending_order = True
                break

        return pending_order

    def has_open_position(self, instrument):
        open_position = False

        # get openn positions from api.
        positions = self.oanda_client.get_open_positions()

        # Check to see if order is already open for this instrument.
        for position in positions:
            if position.instrument == instrument:
                open_position = True
                break

        return open_position

    @staticmethod
    def get_dependencies():
        # oanda rest
        domain, token, account = OandaRest.get_dependencies()
        oar = OandaRest(domain, token, account)

        # oanda client
        api, account_id = OandaClient.get_dependencies()
        oac = OandaClient(api, account_id)

        # twilio
        twilio = _twilio()

        return oar, oac, twilio

    @staticmethod
    def get_dependencies_bt():
        oar = OandaRestBT()
        oac = OandaClientBT()
        twilio = _twilioBT()
        return oar, oac, twilio


def log(message):
    print(message)
