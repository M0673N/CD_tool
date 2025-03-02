from sqlalchemy import Column, String, Integer
from database import Base, engine


class User(Base):
    __tablename__ = "credentials"
    username = Column(String, primary_key=True)
    password = Column(String)


class ScheduledJob(Base):
    __tablename__ = "scheduled_jobs"
    id = Column(Integer, primary_key=True)
    job_name = Column(String)
    job_id = Column(String)


Base.metadata.create_all(engine)
