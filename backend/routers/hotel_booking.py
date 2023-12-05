from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import HotelModel, ItineraryModel
from sqlalchemy.orm import Session
import requests 

router = APIRouter(
    prefix="/hotel_booking",
    tags=['Hotel Bookings']
)

get_db = database.get_db

API_KEY = "1a662e0bdemsh110faa611833139p1cdab6jsn13e9ab23c24f"

@router.get('/', response_model=List[schema.HotelBookingModel])
def all(db: Session = Depends(get_db)):
    return HotelModel.HotelBooking.get_all_hotel_bookings(db)

@router.post('/new_booking/', status_code=status.HTTP_201_CREATED)
def create(request: schema.HotelBookingModel, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    return HotelModel.HotelBooking.create_hotel_booking(request, db)

@router.get('/create/{hotel_id}', status_code=status.HTTP_201_CREATED)
def create_booking(hotel_id: int, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    user_id = current_user.id
    itinerary_id = ItineraryModel.Itinerary.get_user_itinerary_id(user_id, db)
    if itinerary_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not have an itinerary to book a hotel for")
    booking = HotelModel.HotelBooking.create_hotel_booking(schema.HotelBookingModel(hotel_id=hotel_id, itinerary_id=itinerary_id), db)
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel Booking with the hotel id {hotel_id} and itinerary id {itinerary_id} was not found")
    return booking

@router.put('/update_booking/{hotel_id}/{itinerary_id}', status_code=status.HTTP_202_ACCEPTED)
def update(hotel_id, itinerary_id, request: schema.HotelBookingModel, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    booking = HotelModel.HotelBooking.update_hotel_booking(hotel_id, itinerary_id, request, db)
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel Booking with the hotel id {hotel_id} and itinerary id {itinerary_id} was not found")
    return booking

@router.delete('/delete_booking/{hotel_id}/{itinerary_id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(hotel_id, itinerary_id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    booking = HotelModel.HotelBooking.delete_hotel_booking(hotel_id, itinerary_id, db)
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel Booking with the hotel id {hotel_id} and itinerary id {itinerary_id} was not found")
    return booking

@router.get('/get_booking/{hotel_id}/{itinerary_id}', status_code=status.HTTP_200_OK, response_model=schema.HotelBookingModel)
def show(hotel_id, itinerary_id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    booking = HotelModel.HotelBooking.get_hotel_booking(hotel_id, itinerary_id, db)
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel Booking with the hotel id {hotel_id} and itinerary id {itinerary_id} was not found")
    return booking

@router.get('/price/{hotel_id}/{itinerary_id}', status_code=status.HTTP_200_OK, response_model=float)
def get_price(hotel_id, itinerary_id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    booking = HotelModel.HotelBooking.get_hotel_booking(hotel_id, itinerary_id, db)
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel Booking with the hotel id {hotel_id} and itinerary id {itinerary_id} was not found")
    return booking.price

@router.get('/sum_price/{itinerary_id}', status_code=status.HTTP_200_OK, response_model=float)
def get_total_price(itinerary_id: int, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    query = db.query(HotelModel.HotelBooking).join(HotelModel.Hotel).filter(HotelModel.HotelBooking.itinerary_id == itinerary_id).with_entities(HotelModel.HotelBooking.totalPrice).all()
    total_price = sum([booking.totalPrice for booking in query])
    return total_price

