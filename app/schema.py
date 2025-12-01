from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    first_name: str | None = None
    last_name: str | None = None

class User(UserBase):
    id: int
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        orm_mode = True
