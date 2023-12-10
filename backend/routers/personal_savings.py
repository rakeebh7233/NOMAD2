from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import FinanceModel
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/savings",
    tags=['Personal Savings']
)

get_db = database.get_db

@router.get('/', response_model=List[schema.SavingsModel])
def all(db: Session = Depends(get_db)):
    return db.query(FinanceModel.Savings).all()

@router.get('/{email}', response_model=schema.SavingsModel)
def get(email, db: Session = Depends(get_db)):
    response = FinanceModel.Savings.get_savings_user(db, email)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings with email {email} not found")
    return response

@router.post('/new_savings', status_code=status.HTTP_201_CREATED)
def create(request: schema.SavingsCreate, db: Session = Depends(get_db)):
    new_savings = FinanceModel.Savings.create_savings(db, request)
    db.add(new_savings)
    db.commit()
    db.refresh(new_savings)
    return new_savings

@router.put('/update_savings/{email}', status_code=status.HTTP_202_ACCEPTED)
def update(email, request: schema.SavingsCreate, db: Session = Depends(get_db)):
    response = FinanceModel.Savings.update_savings(db, email, request)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings with id {id} not found")
    return 'updated'

@router.put('/add_savings/{email}/{amount}', status_code=status.HTTP_202_ACCEPTED)
def add_savings(email, amount, db: Session = Depends(get_db)):
    response = FinanceModel.Savings.add_savings(db, email, amount)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings with id {id} not found")
    return 'updated'

@router.delete('/delete_savings/{email}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(email, db: Session = Depends(get_db)):
    response = FinanceModel.Savings.delete_savings(db, email)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings with id {id} not found")
    return 'deleted'

@router.get('/find_savings/{email}', status_code=status.HTTP_200_OK, response_model=schema.SavingsModel)
def show(email, db: Session = Depends(get_db)):
    response = FinanceModel.Savings.get_savings_user(db, email)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings with email {email} not found")
    return response

@router.get('/period/{email}', status_code=status.HTTP_200_OK)
def get_period(email, db: Session = Depends(get_db)):
    response = FinanceModel.Savings.get_period(db, email)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings with email {email} not found")
    # print("Router Period: " + response)
    return response

@router.get('/start_date/{email}', status_code=status.HTTP_200_OK)
def get_start_date(email, db: Session = Depends(get_db)):
    response = FinanceModel.Savings.get_start_date(db, email)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings with email {email} not found")
    # print("Router Start Date: " + response)
    return response

@router.get('/update_progress/{email}/{progress}', status_code=status.HTTP_200_OK)
def update_progress_per_period(email, progress, db: Session = Depends(get_db)):
    response = FinanceModel.Savings.update_progress(db, email, progress)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings with email {email} not found")
    print(response.current_budget)
    return response

@router.get('/check_progress/{email}', status_code=status.HTTP_200_OK)
def check_progress(email, db: Session = Depends(get_db)):
    response = FinanceModel.Savings.check_period_success(db, email)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings with email {email} not found")
    return response

@router.get('/check_savings/{email}', status_code=status.HTTP_200_OK)
def check_savings(email, db: Session = Depends(get_db)):
    response = FinanceModel.Savings.check_savings_success(db, email)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings with email {email} not found")
    return response

@router.get('/reset_progress/{email}', status_code=status.HTTP_200_OK)
def reset_progress(email, db: Session = Depends(get_db)):
    response = FinanceModel.Savings.reset_progress_per_period(db, email)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Failed to reset progress")
    return response