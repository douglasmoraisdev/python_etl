from os import listdir
from os.path import isfile, join
import os

import config
from cachecontrol import CacheControl


class Worker:

    FTP_LOCAL_PATH = config.DATASOURCES['ftp_ds']['local_path']
    EXTRACTED_PATH = config.GENERAL['extracted_path']

    # read from downloaded path
    def __read_downloaded(self, work_path):
        return [f for f in listdir(work_path) if isfile(join(work_path, f))]

    # iter on file lines for get latitudes and longitudes
    def __extract_latlong_from_file(self, file_data, timestamp):

        latitude = ''
        longitude = ''
        coords_list = []

        # iter each line
        for index, line in enumerate(file_data):
            # split line in colums
            colums = line.split(' ')

            # latitude line
            if line.startswith('Latitude'):

                # verify this is the begin of the lat/long pair
                if latitude != '':

                    print("[%s] - Inconsistency, no long found [%s:%d]"
                          % (os.getpid(), file, index))

                latitude = colums[4].strip()

            # longitude line
            if line.startswith('Longitude'):

                # verify the pair was closed
                if (longitude == '') and (latitude != ''):

                    # add long to the list
                    longitude = colums[4].strip()

                    # create a new pair
                    coord_pair = {"latitude": latitude,
                                  "longitude": longitude,
                                  "timestamp": timestamp
                                  }

                    # add coord_pair to list
                    coords_list.append(coord_pair)

                    # empty coord pair
                    coord_pair = ()
                    latitude = ''
                    longitude = ''

                else:
                    print("[%s] - Inconsistency, no lat found [%s:%d]"
                          % (os.getpid(), file, index))

                    # empty coord pair
                    coord_pair = ()
                    latitude = ''
                    longitude = ''

        return coords_list

    # Write final extracted file
    def __write_extract_file(self, file_name, coords_list):

        with open(self.EXTRACTED_PATH+file_name, 'w') as f:
            for index, item in enumerate(coords_list):

                # write in ; separated format
                f.write(item["latitude"]+';' +
                        item["longitude"]+';' +
                        item["timestamp"]+'\n')

    # Read all files downloaded
    # Verify for cached files to no process
    # Parses the readed file and write to a uniform format
    # Final extracted file format: (<latitude>;<longitude>;<timestamp>)
    def extract(self):

        # instance cache
        cache = CacheControl()

        # path of downloaded files
        work_path = self.FTP_LOCAL_PATH

        # list to keep all processed files
        files_processed = []

        # Loads all files to work on ftp work path
        work_files = self.__read_downloaded(work_path)

        # process each file
        # list all ftp work files
        timestamp = ''
        for file in work_files:

            # extract timestamp from file
            timestamp = file.split('data_points_')[1].split('.txt')[0]

            # verify the file already processed on cache
            if cache.verify_extracted_cache(file):

                print('[%s] %s not in cache, processing' % (os.getpid(), file))
                # update the cache
                cache.update_extracted_cache(file)

                # load file contents
                file_data = open(work_path+file)

                # extract coords list from file
                coords_list = self.__extract_latlong_from_file(
                    file_data, timestamp)

                # write file in defined format
                self.__write_extract_file(file, coords_list)

                # update processed files list
                files_processed.append(file)

            else:
                print('[%s] %s in cache, no will be processed' %
                      (os.getpid(), file))

        return files_processed
