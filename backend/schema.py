from pydantic import BaseModel

# This file uses pydantic to validate the incoming data from the frontend

# User Schema
class UserBase(BaseModel):
    email_address: str
    firstName: str
    lastName: str

class UserCreate(UserBase):
    hashed_password: str
    class Config:
        orm_mode = True

class UserModel(UserBase):
    id: int
    class Config:
        orm_mode = True





