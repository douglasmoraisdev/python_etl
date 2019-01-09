import time
from multiprocessing import Process
import os

import config
from messagebroker import MessageBroker
from worker import Worker

CICLE_SLEEP_TIME = config.GENERAL['cycle_sleep_time']
MAX_PROCESS = config.GENERAL['max_process']
MAX_GENERAL_ERRORS = config.ERROR_HANDLER['max_general_errors']
GENERAL_ERROR_TIMEOUT = config.ERROR_HANDLER['general_errors_retry_timeout']

TRANSFORMED_PATH = config.GENERAL["transformed_path"]


def loader_sum_def(x, y):
    return x+y

# pre execute tasks function
def pre_execute():

    # create data directories
    if not os.path.isdir(TRANSFORMED_PATH):
        os.makedirs(TRANSFORMED_PATH)


# Loader worker
# runs the loader flow:
# - load to database data on files transformed
def worker(ch, method, properties, body, total_errors=0):

    message_broker = MessageBroker()
    worker = Worker()

    # extract file name from the message queue
    file = body.decode("utf-8").strip()

    print(' ==========> [%s] Cycle start -' % os.getpid())

    if total_errors >= MAX_GENERAL_ERRORS:
        print('max error reached')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # flow
    try:
        worker = worker.load(file)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Fail Safe, in case of Exceptions try again with
    # the MAX_GENERAL_ERRORS limit
    except Exception as e:
        total_errors += 1
        print('A Exception occured[%s]: Waiting to recover %s seconds' % (
            e, GENERAL_ERROR_TIMEOUT))
        time.sleep(GENERAL_ERROR_TIMEOUT)
        worker(ch, method, properties, body, total_errors)

    print(' ==========> [%s] Cycle end -' % os.getpid())
    return


# worker
def main():
    # instance rabbitmq
    message_broker = MessageBroker()

    # start Rabbitmq Listener
    # listening transformer queue
    print('[*] Worker [%s] consuming queue... ' % os.getpid())
    message_broker.consume(callback=worker)


def daemon():

    process_list = []

    for process_index in range(MAX_PROCESS):

        p = Process(target=main)
        p.start()
        process_list.append(p)

    for process_index in range(MAX_PROCESS):

        started_p = process_list[process_index]
        started_p.join()

    print('== ENDED ==')
    print(process_list)


if __name__ == "__main__":

    pre_execute()
    daemon()
