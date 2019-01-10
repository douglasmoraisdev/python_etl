from os import listdir
from os.path import isfile, join
import os
import json

import config
from databaseclient import DatabaseClient
from lookupdbclient import LookupDBClient


class Worker:

    TRANSFORMED_PATH = config.GENERAL['transformed_path']

    # perform loader logic
    # read transformed files,
    # send to database, update or insert depending on previous inserted data
    def load(self, file):

        # instance final database
        dbclient = DatabaseClient()
        # instance auxiliar lookup database
        lookupdb = LookupDBClient()

        work_path = self.TRANSFORMED_PATH

        # open the file
        file_data = open(work_path+file)

        # iter on file lines
        insert_data_list = []
        update_data_list = []

        with open(work_path+file) as json_file:

            file_data = json.load(json_file)

            for item in file_data:

                latitude = item['latitude']
                longitude = item['longitude']

                # verify coordenates already exist on lookup database
                # if exists, add to UPDATE list
                if lookupdb.latlong_exists(latitude, longitude):

                    # append to update list
                    update_data_list.append(item)

                # if not exists, add to INSERT list
                else:

                    # update the lookup database
                    lookupdb.insert_laglong(latitude, longitude)

                    # append colums to list of insert
                    insert_data_list.append(item)

        # show total inserts and updates generated
        print("[%s] %s insert_data [%s]" %
              (os.getpid(), file, len(insert_data_list)))
        print("[%s] %s update_data [%s]" %
              (os.getpid(), file, len(update_data_list)))

        # persist data, do bulk inserts and updates
        dbclient.insert_data(insert_data_list)
        dbclient.update_data(update_data_list)
