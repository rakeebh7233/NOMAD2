from fastapi import APIRouter, HTTPException, security, Depends
from database import db_dependency
import schema
import models

router = APIRouter()

@router.post("/register")
def register(user: schema.UserCreate, db: db_dependency):
    print("registering user")
    db_user = models.User.get_user_by_email(user.email_address, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return models.User.create_user(user,db)

@router.post("/token")
def generate_token(db: db_dependency, form_data: security.OAuth2PasswordRequestForm = Depends()):
    print("generating token")
    user = models.User.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return  models.User.create_token(user)

# @router.get("/user", response_model=schema.UserModel)
# def get_user(user: schema.UserModel = Depends(models.User.get_current_user(db_dependency))):
#     return user