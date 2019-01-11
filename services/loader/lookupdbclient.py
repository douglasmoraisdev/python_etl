import config
from pymongo import MongoClient


class LookupDBClient:

    DB_HOST = config.LOOKUP_DB['db_host']
    DB_PORT = config.LOOKUP_DB['db_port']
    USERNAME = config.LOOKUP_DB['username']
    PASS = config.LOOKUP_DB['password']
    DATABASE = config.LOOKUP_DB['database']

    # Create lookup database connection object
    def __init__(self):

        username = self.USERNAME
        password = self.PASS

        self.client = MongoClient(self.DB_HOST,
                                  username=self.USERNAME,
                                  password=self.PASS,
                                  )
        self.db = self.client[self.DATABASE]



    # insert a new latitude+longitude pair record on lookup database
    def insert_laglong(self, latitude, longitude):

        latlong = self.db.latlong

        rowid = latlong.insert_one({
            "latitude": latitude,
            "longitude": longitude
        }).inserted_id

    # verify the latitude/longitude already exists on lookup database
    def latlong_exists(self, latitude, longitude):

        coord = self.db.latlong.find_one({'latitude': latitude, 'longitude': longitude})

        return coord is not None
