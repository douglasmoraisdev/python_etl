from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    latitude = Column(String)
    longitude = Column(String)
    street_number = Column(String)
    street_name  = Column(String)
    district_name = Column(String)
    city_name = Column(String)
    state_name = Column(String)
    country_name = Column(String)
    postal_code = Column(String)

    def __repr__(self):
       return "<User(latitude='%s', rua='%s', bairro='%s')>" % (
                            self.latitude, self.rua, self.bairro)
