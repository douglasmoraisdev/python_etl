from os import listdir
from os.path import isfile, join
import os

import config
from databaseclient import DatabaseClient
from lookupdbclient import LookupDBClient


class Worker:

    TRANSFORMED_PATH = config.GENERAL['transformed_path']

    # extract data fields from file colums in dict format
    def __format_address(self, line):

        # split line in colums
        colums = line.split(';')

        # format address dict
        address = {
            "latitude": colums[0].strip(),
            "longitude": colums[1].strip(),
            "street_number": colums[2].strip(),
            "street_name": colums[3].strip(),
            "district": colums[4].strip(),
            "city": colums[5].strip(),
            "state": colums[6].strip(),
            "country": colums[7].strip(),
            "postal_code": colums[8].strip()
        }

        return address

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
        for line in file_data:

            address = self.__format_address(line)

            latitude = address['latitude']
            longitude = address['longitude']

            # verify coordenates already exist on lookup database
            # if exists, add to UPDATE list
            if lookupdb.latlong_exists(latitude, longitude):

                # append to update list
                update_data_list.append(address)

            # if not exists, add to INSERT list
            else:

                # update the lookup database
                lookupdb.insert_laglong(latitude, longitude)

                # append colums to list of insert
                insert_data_list.append(address)

        # show total inserts and updates generated
        print("[%s] %s insert_data [%s]" %
              (os.getpid(), file, len(insert_data_list)))
        print("[%s] %s update_data [%s]" %
              (os.getpid(), file, len(update_data_list)))

        # persist data, do bulk inserts and updates
        dbclient.insert_data(insert_data_list)
        dbclient.update_data(update_data_list)
