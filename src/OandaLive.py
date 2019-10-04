from OandaStream import OandaStream
from OandaClient import OandaClient
from Types import Price
from _rabbit import _rabbit
from _redis import _redis

module_name = "OandaLive"
rabbit = _rabbit()
redis = _redis()
oanda_stream = OandaStream()
oanda_client = OandaClient(*OandaClient.get_dependencies())


def publish_price(price_dict):
    price = Price.from_origin(price_dict)
    print(module_name, price.time, price.instrument, price.ask, price.bid)
    price = price.to_json()
    rabbit.publish_live_price(price)


def begin_publish_price_data():
    instruments = oanda_client.get_account_instruments()
    instrument_array = []
    for instrument in instruments:
        print(instrument.name)
        instrument_array.append(instrument.name)

    rabbit.configure_live_price_publish_channel()
    print('oanda_stream')
    oanda_stream.stream(publish_price, instruments=instrument_array)


if __name__ == "__main__":
    print(f"======={module_name}=======")
    begin_publish_price_data()
