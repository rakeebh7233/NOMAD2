from pydantic import BaseModel

# This file uses pydantic to validate 

# User Schema
class User(BaseModel):
    email_address: str
    firstName: str
    lastName: str
    hashed_password: str

