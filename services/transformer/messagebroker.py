import pika

import config


class MessageBroker:

    BROKER_URL = config.MESSAGE_BROKER['broker_url']
    EXTRACTED_QUEUE = config.MESSAGE_BROKER['extracted_queue']
    TRANSFORMER_QUEUE = config.MESSAGE_BROKER['transformed_queue']

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.BROKER_URL))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.TRANSFORMER_QUEUE)

    def consume(self, callback):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(callback,
                                   queue=self.EXTRACTED_QUEUE)

        self.channel.start_consuming()

    def warn_loader(self, file):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.TRANSFORMER_QUEUE,
                                   body=file)

        print(" [x] Sent [%s]" % file)

    def close_connection(self):

        self.connection.close()
