import config
import mysql.connector

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update, and_

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


    def bulk_insert_data(self, insert_list, target):

        bulk_result = self.session.bulk_insert_mappings(target, insert_list)

        self.session.commit()

    def bulk_update_data(self, update_list, target):

        for item in update_list:

            stmt = update(target)\
                    .where(and_(target.latitude==item['latitude'], target.longitude==item['longitude']))\
                    .values(item)

            result = self.session.execute(stmt)

        self.session.commit()
