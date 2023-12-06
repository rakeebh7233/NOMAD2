from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import FinanceModel
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/transactions",
    tags=['Transactions']
)

get_db = database.get_db

@router.get('/', response_model=List[schema.TransactionModel])
def all(db: Session = Depends(get_db)):
    return db.query(FinanceModel.Transaction).all()

@router.post('/new_transaction', status_code=status.HTTP_201_CREATED)
def create(request: schema.TransactionCreate, db: Session = Depends(get_db)):
    new_transaction = FinanceModel.Transaction.create_transaction(request, db)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.get('/find_transaction/{email}', status_code=status.HTTP_200_OK, response_model=schema.TransactionModel)
def show(email, db: Session = Depends(get_db)):
    response = FinanceModel.Transaction.get_transaction_user(email, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with email {email} not found")
    return response

@router.get('/daily/{email}', status_code=status.HTTP_200_OK, response_model=schema.TransactionModel)
def show_daily(email, db: Session = Depends(get_db)):
    response = FinanceModel.Transaction.get_transactions_per_day(email, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with email {email} not found")
    return response

@router.get('/weekly/{email}/{start_date}', status_code=status.HTTP_200_OK, response_model=schema.TransactionModel)
def show_weekly(email, start_date, db: Session = Depends(get_db)):
    response = FinanceModel.Transaction.get_transactions_per_week(email, start_date, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with email {email} not found")
    return response

@router.get('/monthly/{email}/{start_date}', status_code=status.HTTP_200_OK, response_model=schema.TransactionModel)
def show_monthly(email, start_date, db: Session = Depends(get_db)):
    response = FinanceModel.Transaction.get_transactions_per_month(email, start_date, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with email {email} not found")
    return response

@router.get('/yearly/{email}/{start_date}', status_code=status.HTTP_200_OK, response_model=schema.TransactionModel)
def show_yearly(email, start_date, db: Session = Depends(get_db)):
    response = FinanceModel.Transaction.get_transactions_per_year(email, start_date, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with email {email} not found")
    return response
