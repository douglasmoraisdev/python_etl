import config
from pymongo import MongoClient


class LookupDBClient:

    DB_HOST = config.LOOKUP_DB['db_host']
    DB_PORT = config.LOOKUP_DB['db_port']
    USERNAME = config.LOOKUP_DB['username']
    PASS = config.LOOKUP_DB['password']
    DATABASE = config.LOOKUP_DB['database']

    # Create lookup database connection object
    # init latlong_list, used for in-memory compare
    def __init__(self):

        username = self.USERNAME
        password = self.PASS

        self.client = MongoClient(self.DB_HOST,
                                  username=self.USERNAME,
                                  password=self.PASS,
                                  )
        self.db = self.client[self.DATABASE]

        self.latlong_list = []

    # load all latitudes and longitudes on database
    # for in-memory lookup compare
    def __load_latlong(self):

        # iter all coords on lookup database and add to list in tuple format
        for item in self.db.latlong.find({}):
            self.latlong_list.append((item["latitude"], item["longitude"]))

    # insert a new latitude+longitude pair record on lookup database
    def insert_laglong(self, latitude, longitude):

        latlong = self.db.latlong

        rowid = latlong.insert_one({
            "latitude": latitude,
            "longitude": longitude
        }).inserted_id

    # verify the latitude/longitude already exists on lookup database
    def latlong_exists(self, latitude, longitude):

        if len(self.latlong_list) == 0:
            self.__load_latlong()

        return (latitude, longitude) in self.latlong_list
