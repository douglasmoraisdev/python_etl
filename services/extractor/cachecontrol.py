import config
import redis


class CacheControl:

    CACHE_HOST = config.CACHE["host"]
    CACHE_PORT = config.CACHE["port"]
    CACHE_DB = config.CACHE["db"]
    DOWNLOAD_CACHE_PREFIX = config.CACHE["download_cache_prefix"]
    EXTRACTED_CACHE_PREFIX = config.CACHE["extracted_cache_prefix"]

    # create redis connection
    def __init__(self):
        self.cache = redis.Redis(host=self.CACHE_HOST,
                                 port=self.CACHE_PORT,
                                 db=self.CACHE_DB,
                                 )

    # verify cached download files
    def verify_download_cache(self, file):

        return self.cache.get(self.DOWNLOAD_CACHE_PREFIX+file) is None

    # update cache for download files
    def update_download_cache(self, file):

        self.cache.set('download-'+file, '1')

    # verify cached extracted files

    def verify_extracted_cache(self, file):

        return self.cache.get(self.EXTRACTED_CACHE_PREFIX+file) is None

    # update cache for extracted files
    def update_extracted_cache(self, file):

        self.cache.set('extracted-'+file, '1')
