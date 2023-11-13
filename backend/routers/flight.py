from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys 
sys.path.append("..")
import schema, database, models, oauth2
from sqlalchemy.orm import Session
import requests 


router = APIRouter(
    prefix="/flight",
    tags=['Flights']
)

get_db = database.get_db

API_KEY = "1a662e0bdemsh110faa611833139p1cdab6jsn13e9ab23c24f"

@router.get('/', response_model=List[schema.FlightModel])
def all(db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    return db.query(models.Flight).all()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schema.FlightCreate, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    new_flight = models.Flight.create_flight(db, request)
    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)
    return new_flight

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schema.FlightUpdate, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = models.Flight.update_flight(db, id, request)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with id {id} not found")
    return 'updated'

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = models.Flight.delete_flight(db, id)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with id {id} not found")
    return 'deleted'

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schema.FlightModel)
def show(id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = models.Flight.get_flight_by_id(db, id)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with id {id} not found")
    return response

@router.get('/internal_search/{departureAirport}/{arrivalAirport}/{departureTime}/{arrivalTime}', status_code=status.HTTP_200_OK, response_model=schema.FlightModel)
def search_flights_int(departureAirport: str, arrivalAirport: str, departureTime: str, arrivalTime: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = models.Flight.get_flight_by_request(db, departureAirport, arrivalAirport, departureTime, arrivalTime)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to retrieve flights")
    return response

@router.get('/external_search/{departureAirport}/{arrivalAirport}/{departureTime}/{arrivalTime}/{cabinClass}/', status_code=status.HTTP_200_OK, response_model=schema.FlightModel)
def search_flights_ext(departureAirport: str, arrivalAirport: str, departureTime: str, arrivalTime: str, cabinClass: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "booking-com15.p.rapidapi.com"
    }
    params = {
        'departureAirport': departureAirport + '.AIRPORT',
        'arrivalAirport': arrivalAirport + '.AIRPORT',
        'departureTime': departureTime,
        'arrivalTime': arrivalTime,
        'cabinClass': cabinClass
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve flights")
    return response.json()