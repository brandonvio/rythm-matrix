import pika
from Environment import env
from Constants import cons


def get_rabbit_connection():
    username = env.get(cons.RABBIT_USERNAME)
    password = env.get(cons.RABBIT_PASSWORD)
    host = env.get(cons.RABBIT_DOMAIN)
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters
        (
            host=host,
            credentials=credentials
        )
    )
    return connection


def get_rabbit_publish_channel_for_oanda_prices(connection):
    if connection is None:
        connection = get_rabbit_connection()

    # initialize rabbitmq
    channel = connection.channel()
    channel.exchange_declare(exchange=cons.OANDA_PRICE_EXCHANGE, exchange_type='fanout')

    # queue 1
    result = channel.queue_declare(queue=cons.OANDA_PRICE_QUEUE_1)
    channel.queue_bind(exchange=cons.OANDA_PRICE_EXCHANGE, queue=result.method.queue)

    # queue 2
    result = channel.queue_declare(queue=cons.OANDA_PRICE_QUEUE_2)
    channel.queue_bind(exchange=cons.OANDA_PRICE_EXCHANGE, queue=result.method.queue)
    return channel
