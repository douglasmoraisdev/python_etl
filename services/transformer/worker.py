from os import listdir
from os.path import isfile, join
import os
import time

import config
from webclient import WebClient


class Worker:

    EXTRACTED_PATH = config.GENERAL['extracted_path']
    TRANSFORMED_PATH = config.GENERAL['transformed_path']

    # return a dict witi street, city, country, etc, data for a given
    # latitude/longitude pair
    def __enrich_data(self, latitude, longitude):

        webclient = WebClient()
        address = webclient.get_address_by_latlong(latitude, longitude)

        return address

    def __write_transform_file(self, rich_data_list, file_name):
        # write rich data to file
        line = ''
        with open(self.TRANSFORMED_PATH+file_name, 'w') as f:
            for item in rich_data_list:

                # write in ; separated format
                line = \
                    item["latitude"]+';' +\
                    item["longitude"]+';' +\
                    item["street_number"]+';' +\
                    item["road_name"]+';' +\
                    item["district_name"]+';' +\
                    item["city_name"]+';' +\
                    item["state_name"]+';' +\
                    item["country_name"]+';' +\
                    item["postal_code"]+';' +\
                    item["timestamp"]

                f.write(line+'\n')

    # perform transformation logic
    # read extracted files, enrich with external api data and
    # write result on file
    def transform(self, file, proc_index=0):

        work_path = self.EXTRACTED_PATH

        timestamp = file.split('data_points_')[1].split('.txt')[0]

        # open the file
        file_data = open(work_path+file)

        # iter on file lines for get latitudes and longitudes
        rich_data_list = []
        for line in file_data:

            # split line in colums
            colums = line.split(';')

            # get lat and long
            latitude = colums[0].strip()
            longitude = colums[1].strip()

            # call external api for enrich data
            rich_data = self.__enrich_data(latitude, longitude)

            # append file timestamp to rich_data dict
            rich_data["timestamp"] = timestamp

            # append rich dict to list of rich data
            rich_data_list.append(rich_data)

        # write to file
        self.__write_transform_file(rich_data_list, file)

        return file
