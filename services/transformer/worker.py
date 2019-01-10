from os import listdir
from os.path import isfile, join
import os
import time
import json

import config
from webclient import WebClient


class Worker:

    EXTRACTED_PATH = config.GENERAL['extracted_path']
    TRANSFORMED_PATH = config.GENERAL['transformed_path']

    # return a dict with street, city, country, etc, data for a given
    # latitude/longitude pair
    def __enrich_data(self, latitude, longitude):

        webclient = WebClient()
        address = webclient.get_address_by_latlong(latitude, longitude)

        return address

    def __write_transform_file(self, rich_data_list, file_name):

        # write rich data to file
        with open(self.TRANSFORMED_PATH+file_name, 'w') as f:
            json.dump(rich_data_list, f)

    # perform transformation logic
    # read extracted files, enrich with external api data and
    # write result on file
    def transform(self, file, proc_index=0):

        work_path = self.EXTRACTED_PATH

        # iter on file lines for get latitudes and longitudes
        with open(work_path+file) as json_file:
            file_data = json.load(json_file)

            rich_data_list = []
            for item in file_data:

                # get lat and long
                latitude = item['latitude']
                longitude = item['longitude']
                timestamp = item['timestamp']

                # call external api for enrich data
                rich_data = self.__enrich_data(latitude, longitude)

                # append file timestamp to rich_data dict
                rich_data["timestamp"] = timestamp

                # append rich dict to list of rich data
                rich_data_list.append(rich_data)

        # write to file
        self.__write_transform_file(rich_data_list, file)

        return file
