from sqlalchemy import Column, String, Integer
from database import Base


class User(Base):
    __tablename__ = "credentials"
    username = Column(String, primary_key=True, index=True)
    password = Column(String)


class ScheduledJob(Base):
    __tablename__ = "scheduled_jobs"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    hour = Column(Integer)
    minute = Column(Integer)
