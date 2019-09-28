import logging
from flask import Flask, escape, request, jsonify
from flask_cors import CORS
from Oanda import Oanda

# init Oanda.
api, account_id = Oanda.get_dependencies()
oa = Oanda(api, account_id)

# init logger.
logger = logging.getLogger(__name__)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

app = Flask(__name__)
CORS(app)


@app.route('/matrix/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/matrix/api/oanda/account', methods=['GET'])
def get_oanda_account():
    account = oa.get_account_summary()
    return jsonify(account.dict())


if __name__ == "__main__":
    app.run(debug=True)
