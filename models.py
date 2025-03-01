from sqlalchemy import Column, String
from database import Base


class User(Base):
    __tablename__ = "credentials"
    username = Column(String, primary_key=True)
    password = Column(String)
