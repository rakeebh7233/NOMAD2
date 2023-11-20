from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import FinanceModel
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/finance",
    tags=['Personal Finance']
)

get_db = database.get_db

@router.get('/', response_model=List[schema.FinanceModel])
def all(db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    return db.query(FinanceModel.PersonalFinance).all()

@router.post('/new_finance/', status_code=status.HTTP_201_CREATED)
def create(request: schema.FinanceCreate, db: Session = Depends(get_db)):
    new_finance = FinanceModel.PersonalFinance.create_finance(db, request)
    db.add(new_finance)
    db.commit()
    db.refresh(new_finance)
    return new_finance

@router.put('/update_finance/{email}', status_code=status.HTTP_202_ACCEPTED)
def update(email, request: schema.FinanceUpdate, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FinanceModel.PersonalFinance.update_finance(db, email, request)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Finance with email {email} not found")
    return 'updated'

@router.delete('/delete_finance/{email}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(email, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FinanceModel.PersonalFinance.delete_finance(db, email)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Finance with email {email} not found")
    return 'deleted'

@router.get('/find_finance_user/{email}', status_code=status.HTTP_200_OK, response_model=schema.FinanceModel)
def show(email, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FinanceModel.PersonalFinance.get_finance_user(db, email)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Finance with email {email} not found")
    return response
