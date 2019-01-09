import ftputil
import os

import config
from cachecontrol import CacheControl


class FtpClient:

    FTP_URL = config.DATASOURCES['ftp_ds']['url']
    FTP_USERNAME = config.DATASOURCES['ftp_ds']['username']
    FTP_PASSWORD = config.DATASOURCES['ftp_ds']['password']
    FTP_LOCAL_PATH = config.DATASOURCES['ftp_ds']['local_path']

    # create ftp connection
    def __init__(self):
        self.ftp_client = ftputil.FTPHost(
            self.FTP_URL, self.FTP_USERNAME, self.FTP_PASSWORD)

    def __list_ftp_files(self):
        return self.ftp_client.listdir(self.ftp_client.curdir)

    def __download_no_cached_file(self, file, cache):

        # verify ftp record is file
        if self.ftp_client.path.isfile(file):

            # verify dowloaded cache
            if cache.verify_download_cache(file):
                print('[%s] %s not in cache, downloading...' %
                      (os.getpid(), file))

                # create cache file to block others
                # to download the same file
                cache.update_download_cache(file)

                # download file
                self.ftp_client.download(file, self.FTP_LOCAL_PATH + file)
                print('[%d] - downloaded [%s]' % (os.getpid(), file))

            else:
                print('[%s] %s in cache, no will be downloaded' %
                      (os.getpid(), file))

    # list all files in the home dir of the ftp host
    # and download all files, using cache
    def download_files(self):

        # cache instance
        cache = CacheControl()

        # list ftp dir
        file_names = self.__list_ftp_files()

        # iter over ftp home dir records (paths, ., .., files)
        for file in file_names:

            # download file
            self.__download_no_cached_file(file, cache)

        return True

    def close_connection(self):

        self.ftp_client.quit()
