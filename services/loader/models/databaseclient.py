import config
import mysql.connector

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseClient:


    DB_HOST = config.DATABASE['db_host']
    USERNAME = config.DATABASE['username']
    PASS = config.DATABASE['password']
    DATABASE = config.DATABASE['database']

    def __init__(self):

        engine = create_engine("mysql+mysqlconnector://%s:%s@%s:3306/%s" % (
            self.USERNAME,
            self.PASS,
            self.DB_HOST,
            self.DATABASE)
        )

        DBSession = sessionmaker(bind=engine)

        # db object
        self.session = DBSession()


    def bulk_insert_data(self, insert_address, target):

        self.session.bulk_insert_mappings(target, insert_address)

        self.session.commit()

        '''
        cursor = self.db.cursor()

        for item in insert_address:

            sql = "INSERT INTO address (latitude, longitude, numero, \
                                        rua, bairro, cidade, estado, \
                                        pais, cep) \
                                        VALUES (%s, %s, %s, %s, %s,\
                                        %s, %s, %s, %s)"
            values = (item["latitude"], item["longitude"],
                      item["street_number"],
                      item["street_name"], item["district_name"], item["city_name"],
                      item["state_name"], item["country_name"], item["postal_code"])
            cursor.execute(sql, values)

        self.db.commit()
        '''

    def update_data(self, update_address):

        cursor = self.db.cursor()

        for item in update_address:

            sql = "UPDATE address SET \
                   numero=%s, \
                   rua=%s, bairro=%s, cidade=%s, estado=%s, \
                   pais=%s, cep=%s \
                   WHERE (latitude=%s and longitude=%s)"
            values = (item["street_number"],
                      item["street_name"], item["district_name"], item["city_name"],
                      item["state_name"], item["country_name"], item["postal_code"],
                      item["latitude"], item["longitude"])
            cursor.execute(sql, values)

        self.db.commit()
