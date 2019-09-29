import pymongo
from pymongo import MongoClient
from Environment import get_env
from Constants import env
from _time import _time


class _mongo:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uri = get_env(env.MONGODB_FULL_URL)
        self.client = MongoClient(uri)

    def get_data_from_oanda_stream(self, record_limit):
        print("get_data_from_oanda_stream")
        result = self.client.matrix_data.oanda_stream.find(
            {
                'time': {
                    '$gt': "2019-09-17T06:00:00Z",
                    '$lt': "2019-09-17T14:00:00Z"
                },
                'instrument': 'EUR_USD'
            },
            limit=record_limit)
        return result

    def get_testing_price_data(self):
        print("get_testing_price_data")
        result = self.client.matrix_data.oanda_stream.find(
            {
                'time': {
                    '$gt': "2019-09-16T00:00:00Z",
                    '$lt': "2019-09-17T00:00:00Z"
                },
                'instrument': 'EUR_USD'
            }).sort("time", pymongo.DESCENDING)

        price_list = list(result)
        return price_list

    def log(self, message, log_type):
        print(message)
        utc_now = _time.utc_now_localized()
        log = {
            "log_date": utc_now,
            "log_type": log_type,
            "message": message
        }
        self.client.matrix_log.insert(log)


if __name__ == "__main__":
    mongo = _mongo()
    test = list(mongo.get_testing_price_data())
    print(test)
    print(len(test))
