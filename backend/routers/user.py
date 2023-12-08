from fastapi import APIRouter, HTTPException, security, Depends
from datetime import datetime, timedelta
from database import db_dependency
import schema
from models import UserModel

router = APIRouter()

@router.post("/register")
def register(user: schema.UserCreate, db: db_dependency):
    print("registering user")
    db_user = UserModel.User.get_user_by_email(user.email_address, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    access_token_expires = timedelta(minutes=30)
    user = UserModel.User.create_user(user,db)
    access_token = UserModel.User.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=schema.Token)
def login(db: db_dependency, form_data: security.OAuth2PasswordRequestForm = Depends()):
    print("generating token") 
    user = UserModel.User.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=120)
    access_token = UserModel.User.create_access_token(data={"sub": user.email_address}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schema.UserModel)
def get_user(user: schema.UserModel = Depends(UserModel.User.get_current_user)):
    return user 