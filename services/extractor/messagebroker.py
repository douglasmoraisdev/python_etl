import pika

import config


class MessageBroker:

    BROKER_URL = config.MESSAGE_BROKER['broker_url']
    BROKER_QUEUE = config.MESSAGE_BROKER['broker_queue']
    BROKER_ROUTING_KEY = config.MESSAGE_BROKER['broker_routing_key']

    # Create Rabbitmq connectioni
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.BROKER_URL))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.BROKER_QUEUE)

    # Send a message to Transformer Queue
    # Message format: "filename.txt"
    def warn_transformer(self, processed_files):

        # iter all processed files and send message for each
        for itens in processed_files:
            self.channel.basic_publish(exchange='',
                                       routing_key=self.BROKER_ROUTING_KEY,
                                       body=itens)

            print(" [x] Sent [%s]" % itens)

    # Close Rabbitmq connection
    def close_connection(self):

        self.connection.close()
