import pika
from Environment import env
from Constants import cons


class RabbitHelper:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oanda_publish_channel = None

    def get_connection(self):
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

    def configure_oanda_publish_channel(self):
        # initialize rabbitmq
        connection = self.get_connection()
        channel = connection.channel()
        channel.exchange_declare(exchange=cons.OANDA_PRICE_EXCHANGE, exchange_type='fanout')

        # queue 1
        result = channel.queue_declare(queue=cons.OANDA_PRICE_QUEUE_1)
        channel.queue_bind(exchange=cons.OANDA_PRICE_EXCHANGE, queue=result.method.queue)

        # queue 2
        result = channel.queue_declare(queue=cons.OANDA_PRICE_QUEUE_2)
        channel.queue_bind(exchange=cons.OANDA_PRICE_EXCHANGE, queue=result.method.queue)
        self.oanda_publish_channel = channel

    def publish_oanda_price(self, price):
        self.oanda_publish_channel.basic_publish(exchange=cons.OANDA_PRICE_EXCHANGE,
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
