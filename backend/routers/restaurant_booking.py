from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import RestaurantModel

from sqlalchemy.orm import Session
import requests 

router = APIRouter(
    prefix="/restaurant_booking",
    tags=['Restaurant Bookings']
)

get_db = database.get_db

@router.get('/', response_model=List[schema.RestaurantBookingModel])
def all(db: Session = Depends(get_db)):
    return RestaurantModel.RestaurantBooking.get_all_restaurant_bookings(db)

@router.post('/new_booking', status_code=status.HTTP_201_CREATED)
def create(request: schema.RestaurantBookingModel, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    return RestaurantModel.RestaurantBooking.create_restaurant_booking(request, db)

@router.put('/update_booking/{geoID}/{restaurantName}/{itinerary_id}', status_code=status.HTTP_202_ACCEPTED)
def update(geoID, restaurantName, itinerary_id, request: schema.RestaurantBookingModel, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    booking = RestaurantModel.RestaurantBooking.update_restaurant_booking(geoID, restaurantName, itinerary_id, request, db)
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant Booking was not found")
    return booking

@router.delete('/delete_booking/{geoID}/{restaurantName}/{itinerary_id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(geoID, restaurantName, itinerary_id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    booking = RestaurantModel.RestaurantBooking.delete_flight_booking(geoID, restaurantName, itinerary_id, db)
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant Booking was not found")
    return booking

@router.get('/find_booking/{geoID}/{restaurantName}/{itinerary_id}', status_code=status.HTTP_200_OK, response_model=schema.RestaurantBookingModel)
def show(geoID, restaurantName, itinerary_id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    booking = RestaurantModel.RestaurantBooking.get_flight_booking(geoID, restaurantName, itinerary_id, db)
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant Booking was not found")
    return booking