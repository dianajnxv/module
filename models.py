from sqlalchemy import Column, ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, index=True)
    second_name = Column(String, index=True)
    email = Column(String, unique=True)
    password = Column(String)

    records = relationship("Record", back_populates="user")


class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="records")
