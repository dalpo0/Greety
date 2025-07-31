import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    join_date = Column(DateTime, default=datetime.utcnow)

class Database:
    def __init__(self, connection_url):
        self.engine = create_engine(connection_url, pool_pre_ping=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def log_location(self, user_id, username, first_name, lat, lng):
        with self.Session() as session:
            user = session.merge(User(
                id=user_id,
                username=username,
                first_name=first_name,
                latitude=lat,
                longitude=lng
            ))
            session.commit()
            return user
