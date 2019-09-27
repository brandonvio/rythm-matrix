import pandas as pd
from ColorPrint import *
from _twilio import _twilio
from _time import _time

twilio = _twilio()


class Trader:
    def __init__(self):
        self._take_profit_pips = 0.0001
        self._stop_loss_pips = 0.0005

    def create_position(self, ask, bid, instrument_id, position_size, the_signal):
        if self.has_open_postion(instrument_id):
            log(f"Position already open for {instrument_id}. No trade.")
            return False

        # Based on long (1) or short (-1) configure trade parameters.
        if the_signal == 1:
            amount_for_stop_loss = self._stop_loss_pips
            amount_for_take_profit = self._take_profit_pips
            position_size = position_size
            stop_loss = round(bid - amount_for_stop_loss, 5)
            take_profit = round(ask + amount_for_take_profit, 5)
            the_price = round(ask, 5)
        elif the_signal == -1:
            amount_for_stop_loss = self._stop_loss_pips * -1
            amount_for_take_profit = self._take_profit_pips * -1
            position_size = position_size * -1
            stop_loss = round(ask - amount_for_stop_loss, 5)
            take_profit = round(bid + amount_for_take_profit, 5)
            the_price = round(bid, 5)

        # Place the order.
        the_time = str(_time.utc_now())

        # TODO replace broker api with Oanda.
        result = self._broker_api.place_limit_order(
            instrument_id,
            the_price,
            stop_loss,
            take_profit,
            position_size,
            the_time)

        if result:
            message = f"Success. Market order placed for {instrument_id} with stop loss of {stop_loss} and take profit of {take_profit}."
            twilio.send_message(message)
        else:
            message = f"Failure. Market order failed for {instrument_id} with stop loss of {stop_loss} and take profit of {take_profit}."
            twilio.send_message(message)
        return True

    def has_open_position(self, instrument_id):
        open_position = False
        # get openn positions from api.
        positions = self._broker_api.get_open_positions()

        # Check to see if position is already open for this instrument.
        for position in positions:
            log(position["instrument"])
            if position["instrument"] == instrument_id:
                open_position = True
                break

        return open_position


def log(message):
    print(message)
