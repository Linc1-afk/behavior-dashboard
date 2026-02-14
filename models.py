from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class BehaviorHistory(Base):
    __tablename__ = "behavior_history"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    timestamp = Column(DateTime)
    activity = Column(String)
    score = Column(Integer)
    state = Column(String)