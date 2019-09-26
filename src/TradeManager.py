import pika
import pickle
import collections
import pandas as pd
from Types import Price


queue_name = 'oanda_prices_q_2'
credentials = pika.PlainCredentials('springcloud', '123456')
connection = pika.BlockingConnection(
    pika.ConnectionParameters
    (
        host='localhost',
        credentials=credentials
    )
)
channel = connection.channel()
channel.queue_declare(queue=queue_name)
price_list = []


def callback(ch, method, properties, body):
    price = pickle.loads(body)
    print("TradeManager", price)
    price_list.append(price)
    df = pd.DataFrame(price_list)
    print(len(df))


channel.basic_consume(queue=queue_name,
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
