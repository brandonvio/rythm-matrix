import pymongo
from pymongo import MongoClient
from Types import price_from_dict
from Environment import env
from Constants import cons


def get_data_from_oanda_stream(record_limit):
    print("get_testing_price_data")
    client = get_mongo_client()
    result = client.matrix_data.oanda_stream.find(
        {
            'time': {
                '$gt': "2019-09-17T00:00:00Z",
                '$lt': "2019-09-17T09:00:00Z"
            },
            'instrument': 'EUR_USD'
        },
        limit=10)
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
    uri = env.get(cons.MONGODB_FULL_URL)
    client = MongoClient(uri)
    return client


if __name__ == "__main__":
    test = list(get_testing_price_data())
    print(test)
    print(len(test))
