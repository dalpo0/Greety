import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)

class Database:
    def __init__(self, connection_url):
        self.engine = create_engine(connection_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def log_location(self, user_id, lat, lng):
        with self.Session() as session:
            session.merge(User(id=user_id, latitude=lat, longitude=lng))
            session.commit()
