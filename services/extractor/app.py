import time
from multiprocessing import Process
import os

import config
from ftpclient import FtpClient
from messagebroker import MessageBroker
from worker import Worker

CICLE_SLEEP_TIME = config.GENERAL['cycle_sleep_time']
MAX_GENERAL_ERRORS = config.ERROR_HANDLER['max_general_errors']
GENERAL_ERROR_TIMEOUT = config.ERROR_HANDLER['general_errors_retry_timeout']


def create_work_paths(extracted_path, ftp_path):

    # create final extracted files path
    if not os.path.isdir(extracted_path):
        os.mkdir(extracted_path)

    # create ftp work path
    if not os.path.isdir(ftp_path):
        os.mkdir(ftp_path)


# pre execute tasks function
def pre_execute(config):

    try:

        create_work_paths(config.GENERAL["extracted_path"],
                          config.DATASOURCES['ftp_ds']['local_path'])

    except Exception as e:
        print('Error on pre_execute: %s' % e)
        return False

    return True

# Extractor worker
# runs in sequence the extractor flow:
# 1 - download ftp files
# 2 - processed files downloaded
# 3 - warn progress to transformer service
def worker(ftp_client, message_broker, worker, loop=True):

    total_errors = 0

    # Runs until total_errors reached
    while True:

        print(' ==========> Cycle start -', os.getpid())

        if total_errors >= MAX_GENERAL_ERRORS:
            print('max error reached')
            break

        # flow
        try:
            ftp_client.download_files()
            processed_files = worker.extract()
            message_broker.warn_transformer(processed_files)

        # Fail Safe, in case of Exceptions try again with
        # the MAX_GENERAL_ERRORS limit
        except Exception as e:
            total_errors += 1
            print('A Exception occured[%s]: Waiting to recover %s seconds' % (
                e, GENERAL_ERROR_TIMEOUT))

            if loop:
                time.sleep(GENERAL_ERROR_TIMEOUT)

        print(' ==========> Cycle end -', os.getpid())

        if loop:
            time.sleep(CICLE_SLEEP_TIME)
        else:
            break



            
# Run the subprocess workers
def daemon(config):

    process_list = []

    # iter for create max avaliable process(threads)
    for process_index in range(config.GENERAL['max_process']):

        # assing and subprocess
        p = Process(target=worker, args = (FtpClient(), MessageBroker(), Worker()))
        p.start()

        # list to be joined later
        process_list.append(p)

    # join all subprocess
    for process_index in range(config.GENERAL['max_process']):

        started_p = process_list[process_index]
        started_p.join()

    print(process_list)


# main service entry point
if __name__ == "__main__":

    pre_execute(config)
    daemon(config)
    print('== Service ENDED ==')
