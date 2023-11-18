from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import FlightModel
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
    return db.query(FlightModel.Flight).all()

@router.post('/new_flight/', status_code=status.HTTP_201_CREATED)
def create(request: schema.FlightCreate, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    new_flight = FlightModel.Flight.create_flight(db, request)
    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)
    return new_flight

@router.put('/update_flight/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schema.FlightUpdate, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FlightModel.Flight.update_flight(db, id, request)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with id {id} not found")
    return 'updated'

@router.delete('/delete_flight/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FlightModel.Flight.delete_flight(db, id)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with id {id} not found")
    return 'deleted'

@router.get('/find_flight_id/{id}', status_code=status.HTTP_200_OK, response_model=schema.FlightModel)
def show(id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FlightModel.Flight.get_flight_by_id(db, id)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with id {id} not found")
    return response

@router.get('/internal_search/{departureAirport}/{arrivalAirport}/{departureTime}/{arrivalTime}', status_code=status.HTTP_200_OK, response_model=schema.FlightModel)
def search_flights_int(departureAirport: str, arrivalAirport: str, departureTime: str, arrivalTime: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FlightModel.Flight.get_flight_by_request(db, departureAirport, arrivalAirport, departureTime, arrivalTime)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to retrieve flights")
    return response

@router.get('/external_search/{departureAirport}/{arrivalAirport}/{departureTime}/{arrivalTime}/{cabinClass}', status_code=status.HTTP_200_OK, response_model=schema.FlightModel)
def search_flights_ext(departureAirport: str, arrivalAirport: str, departureTime: str, arrivalTime: str, cabinClass: str, db: Session = Depends(get_db)):
    
    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"
    querystring = {"fromId":departureAirport + ".AIRPORT",
                   "toId":arrivalAirport + ".AIRPORT",
                   "departDate":departureTime,
                   "returnDate":arrivalTime,
                   "cabinClass":cabinClass,
                   "currency_code":"USD"}
    headers = {
        "X-RapidAPI-Key": "1a662e0bdemsh110faa611833139p1cdab6jsn13e9ab23c24f",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        print("Call Failed for Flights API")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve flights")
    print("Call Successful for Flights API")
    #Cachine Flights in Database
    flights = response.json()['data']['flightOffers']
    flights_list = []
    for flight in flights:
        flight_model = schema.FlightCreate(
            departureAirport=flight['segments'][0]['departureAirport']['code'],
            arrivalAirport=flight['segments'][0]['arrivalAirport']['code'],
            departureTime=flight['segments'][0]['departureTime'][0:11],
            arrivalTime=flight['segments'][0]['arrivalTime'][0:11],
            cabinClass=flight['segments'][0]['legs'][0]['cabinClass'],
            carrier=flight['segments'][0]['legs'][0]['carriers'][0],
            totalPrice=flight['priceBreakdown']['total']['units']
        )
        flights_list.append(flight_model)
    cache_flights(flights_list, db)
    print("Flights from external API cached in database")

    return response.json()

def cache_flights(flights: List[schema.FlightCreate], db: Session = Depends(get_db)):
    for flight in flights:
        new_flight = FlightModel.Flight.create_flight(db, flight)
        db.add(new_flight)
        db.commit()
        db.refresh(new_flight)
    return flights