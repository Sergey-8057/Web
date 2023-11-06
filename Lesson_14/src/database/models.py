from sqlalchemy import Boolean, Column, Date, Integer, String, func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import declarative_base, relationship


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
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="humans")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    humans = relationship("Human", back_populates="user")
    confirmed = Column(Boolean, default=False)
