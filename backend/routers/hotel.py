from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys 
sys.path.append("..")
import schema, database, models, oauth2
from sqlalchemy.orm import Session
import requests 

router = APIRouter(
    prefix="/hotel",
    tags=['Hotels']
)

get_db = database.get_db

API_KEY = "1a662e0bdemsh110faa611833139p1cdab6jsn13e9ab23c24f"

@router.get('/', response_model=List[schema.HotelModel])
def all(db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    return db.query(models.Hotel).all()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schema.HotelCreate, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    new_hotel = models.Hotel.create_hotel(db, request)
    db.refresh(new_hotel)
    return new_hotel

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schema.HotelCreate, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = models.Hotel.update_hotel(db, id, request)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {id} not found")
    return 'updated'

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = models.Hotel.delete_hotel(db, id)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {id} not found")
    return 'deleted'

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def show(id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = models.Hotel.get_hotel_by_id(db, id)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {id} not found")
    return hotel

@router.get('/{name}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def search_hotels(name: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = models.Hotel.get_hotel_by_name(db, name)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with name {name} not found")
    return hotel

@router.get('/{location}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def search_hotels(location: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = models.Hotel.get_hotel_by_location(db, location)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with location {location} not found")
    return hotel

@router.get('/search/{location}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def search_hotels_external(location: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    url = "https://hotels4.p.rapidapi.com/locations/search"
    querystring = {"query":location,"locale":"en_US"}
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with location {location} not found")
    return response.json()

