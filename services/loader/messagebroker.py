import pika

import config


class MessageBroker:

    BROKER_URL = config.MESSAGE_BROKER['broker_url']
    BROKER_QUEUE = config.MESSAGE_BROKER['broker_queue']
    BROKER_ROUTING_KEY = config.MESSAGE_BROKER['broker_routing_key']

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.BROKER_URL))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.BROKER_QUEUE)

    def consume(self, callback):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(callback,
                                   queue=self.BROKER_QUEUE)

        self.channel.start_consuming()

    def warn_loader(self, processed_files):

        for itens in processed_files:
            self.channel.basic_publish(exchange='',
                                       routing_key=self.BROKER_ROUTING_KEY,
                                       body=itens)

            print(" [x] Sent [%s]" % itens)

    def close_connection(self):

        self.connection.close()
