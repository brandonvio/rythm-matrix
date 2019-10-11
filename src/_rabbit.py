import pika
from Environment import get_env
from Constants import env


class _rabbit:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oanda_publish_channel = None
        self.live_price_channel = None

    def get_connection(self):
        username = get_env(env.RABBIT_USERNAME)
        password = get_env(env.RABBIT_PASSWORD)
        host = get_env(env.RABBIT_DOMAIN)
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters
            (
                host=host,
                credentials=credentials
            )
        )
        return connection

    def configure_oanda_publish_channel(self):
        # initialize rabbitmq
        connection = self.get_connection()
        channel = connection.channel()
        channel.exchange_declare(
            exchange=env.OANDA_PRICE_EXCHANGE, exchange_type='fanout')

        # queue 1
        result = channel.queue_declare(queue=env.OANDA_PRICE_QUEUE_1)
        channel.queue_bind(exchange=env.OANDA_PRICE_EXCHANGE,
                           queue=result.method.queue)

        # queue 2
        result = channel.queue_declare(queue=env.OANDA_PRICE_QUEUE_2)
        channel.queue_bind(exchange=env.OANDA_PRICE_EXCHANGE,
                           queue=result.method.queue)

        # queue 3
        result = channel.queue_declare(queue=env.OANDA_PRICE_QUEUE_3)
        channel.queue_bind(exchange=env.OANDA_PRICE_EXCHANGE,
                           queue=result.method.queue)

        self.oanda_publish_channel = channel

    def publish_oanda_price(self, price):
        self.oanda_publish_channel.basic_publish(exchange=env.OANDA_PRICE_EXCHANGE,
                                                 routing_key='',
                                                 body=price)

    def get_oanda_consume_channel(self, queue_name, callback):
        connection = self.get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_consume(queue=queue_name,
                              auto_ack=True,
                              on_message_callback=callback)
        return channel

    # Oanda Live

    def configure_live_price_publish_channel(self):
        # initialize rabbitmq
        connection = self.get_connection()
        channel = connection.channel()
        channel.exchange_declare(
            exchange=env.LIVE_PRICE_EXCHANGE, exchange_type='fanout')

        # queue 1
        result = channel.queue_declare(queue=env.LIVE_PRICE_QUEUE_1)
        channel.queue_bind(exchange=env.LIVE_PRICE_EXCHANGE,
                           queue=result.method.queue)

        self.live_price_channel = channel

    def publish_live_price(self, price):
        # print("publish_live_price", price)
        self.live_price_channel.basic_publish(exchange=env.LIVE_PRICE_EXCHANGE,
                                              routing_key='',
                                              body=price)
