from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///users.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

Base.metadata.create_all(engine)


def get_session():
    return Session()
