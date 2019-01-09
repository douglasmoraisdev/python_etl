import config
import mysql.connector


class DatabaseClient:

    DB_HOST = config.DATABASE['db_host']
    USERNAME = config.DATABASE['username']
    PASS = config.DATABASE['password']
    DATABASE = config.DATABASE['database']

    def __init__(self):
        self.db = mysql.connector.connect(
            host=self.DB_HOST,
            user=self.USERNAME,
            passwd=self.PASS,
            database=self.DATABASE
        )

    def insert_data(self, insert_address):

        cursor = self.db.cursor()

        for item in insert_address:

            sql = "INSERT INTO address (latitude, longitude, numero, \
                                        rua, bairro, cidade, estado, \
                                        pais, cep) \
                                        VALUES (%s, %s, %s, %s, %s,\
                                        %s, %s, %s, %s)"
            values = (item["latitude"], item["longitude"],
                      item["street_number"],
                      item["street_name"], item["district"], item["city"],
                      item["state"], item["country"], item["postal_code"])
            cursor.execute(sql, values)

        self.db.commit()

    def update_data(self, update_address):

        cursor = self.db.cursor()

        for item in update_address:

            sql = "UPDATE address SET \
                   numero=%s, \
                   rua=%s, bairro=%s, cidade=%s, estado=%s, \
                   pais=%s, cep=%s \
                   WHERE (latitude=%s and longitude=%s)"
            values = (item["street_number"],
                      item["street_name"], item["district"], item["city"],
                      item["state"], item["country"], item["postal_code"],
                      item["latitude"], item["longitude"])
            cursor.execute(sql, values)

        self.db.commit()
