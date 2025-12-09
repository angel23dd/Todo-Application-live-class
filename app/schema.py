from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    first_name: Optional [str ] = None
    last_name: Optional [str ] = None


class Login(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: int
    first_name: Optional [str ] = None
    last_name: str | None = None

    class Config:
      from_attributes = True

class TodoBase(BaseModel):
    title:str
    subtitle:Optional [str] =None
    description:str
    owner_id:int


   
    
class TodoCreate(TodoBase):
    date: date
    time: time
    completed: bool = False


class TodoUpdate(BaseModel):
    title:Optional[str] = None
    subtitle:Optional[str] = None
    description:Optional[str] = None
    date:Optional[date] = None
    time: Optional[time] = None
    completed: Optional[bool] = None


class ReadTodo(TodoBase):
    id: int
    title:str 
    subtitle:str 
    description:str
    date: date 
    time: time
    completed: bool 
    class Config:
        from_attributes = True

class DeleteTodo (BaseModel):
    message: str 
   
    