from sqlalchemy import Column, Integer, String, Boolean, Date, Time
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(15), nullable=False)
    last_name = Column(String(10), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String,nullable=False)
    is_verified = Column(Boolean, default=False)

class Otp(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    otp_code = Column(String, nullable=False)


class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,nullable=False)
    subtitle = Column (String,nullable=True)
    description = Column(String,nullable=False)
    owner_id = Column(Integer,nullable=False,index=True)
    date = Column(Date,nullable=False)
    time = Column(Time,nullable=False)
    completed = Column(Boolean, default=False,nullable=False)
   
