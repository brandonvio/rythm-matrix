import pymongo
from pymongo import MongoClient
from Types import price_from_dict
from Environment import get_env
from Constants import env


def get_data_from_oanda_stream(record_limit):
    print("get_testing_price_data")
    client = get_mongo_client()
    result = client.matrix_data.oanda_stream.find(
        {
            'time': {
                '$gt': "2019-09-17T06:00:00Z",
                '$lt': "2019-09-17T14:00:00Z"
            },
            'instrument': 'EUR_USD'
        },
        limit=record_limit)
    return result


def get_testing_price_data():
    print("get_testing_price_data")
    client = get_mongo_client()
    result = client.matrix_data.oanda_stream.find(
        {
            'time': {
                '$gt': "2019-09-16T00:00:00Z",
                '$lt': "2019-09-17T00:00:00Z"
            },
            'instrument': 'EUR_USD'
        }).sort("time", pymongo.DESCENDING)

    _list = list(result)
    price_list = []
    for _price in _list:
        price_list.append(price_from_dict(_price))
    return price_list


def get_mongo_client():
    uri = get_env(env.MONGODB_FULL_URL)
    client = MongoClient(uri)
    return client


if __name__ == "__main__":
    test = list(get_testing_price_data())
    print(test)
    print(len(test))
