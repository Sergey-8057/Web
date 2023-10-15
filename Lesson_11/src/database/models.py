from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Human(Base):
    __tablename__ = "humans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    birthday = Column(Date)
    description = Column(String, default=None)
