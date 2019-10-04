import json
import requests
from Constants import env
from Environment import get_env


class OandaStream:
    def stream(self, callback, instruments=None):
        accountID = get_env(env.OANDA_DEFAULT_ACCOUNT)
        token = get_env(env.OANDA_TOKEN)
        headers = {"Authorization": f"Bearer {token}"}
        if instruments is None:
            instruments = ["EUR_USD", "USD_JPY", "AUD_USD", "USD_CAD", "USD_CHF", "USD_JPY", "EUR_JPY", "GBP_USD"]

        instrument_url = ""
        for instrument in instruments:
            instrument_url = instrument_url + f"{instrument}%2C"

        stream_domain = get_env(env.OANDA_STREAM_DOMAIN)
        the_url = f"https://{stream_domain}/v3/accounts/{accountID}/pricing/stream?instruments={instrument_url}"
        r = requests.get(the_url, stream=True, headers=headers)

        print(">>>> Pricing service online! <<<<<")
        for line in r.iter_lines():
            if line:
                line = json.loads(line.decode('utf-8'))
                if line["type"] == "PRICE":
                    callback(line)
