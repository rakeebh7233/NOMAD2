from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import FlightModel

from sqlalchemy.orm import Session
import requests 

router = APIRouter(
    prefix="/flight_booking",
    tags=['Flight Bookings']
)

get_db = database.get_db

@router.get('/', response_model=List[schema.FlightBookingModel])
def all(db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    return FlightModel.FlightBooking.get_all_flight_bookings(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schema.FlightBookingModel, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    return FlightModel.FlightBooking.create_flight_booking(request, db)

@router.put('/{flight_id}/{itinerary_id}', status_code=status.HTTP_202_ACCEPTED)
def update(flight_id, itinerary_id, request: schema.FlightBookingModel, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    booking = FlightModel.FlightBooking.update_flight_booking(flight_id, itinerary_id, request, db)
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight Booking with the flight id {flight_id} and itinerary id {itinerary_id} was not found")
    return booking

@router.delete('/{flight_id}/{itinerary_id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(flight_id, itinerary_id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    booking = FlightModel.FlightBooking.delete_flight_booking(flight_id, itinerary_id, db)
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight Booking with the flight id {flight_id} and itinerary id {itinerary_id} was not found")
    return booking

@router.get('/{flight_id}/{itinerary_id}', status_code=status.HTTP_200_OK, response_model=schema.FlightBookingModel)
def show(flight_id, itinerary_id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    booking = FlightModel.FlightBooking.get_flight_booking(flight_id, itinerary_id, db)
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight Booking with the flight id {flight_id} and itinerary id {itinerary_id} was not found")
    return booking

@router.get('/{flight_id}/{itinerary_id}/price', status_code=status.HTTP_200_OK, response_model=schema.FlightBookingModel)
def get_price(flight_id, itinerary_id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    booking = FlightModel.FlightBooking.get_flight_booking(flight_id, itinerary_id, db)
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight Booking with the flight id {flight_id} and itinerary id {itinerary_id} was not found")
    return booking.price