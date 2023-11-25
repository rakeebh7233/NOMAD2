from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from config import settings
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import HotelModel
from sqlalchemy.orm import Session
import requests 

router = APIRouter(
    prefix="/hotel",
    tags=['Hotels']
)

get_db = database.get_db

API_KEY = settings.API_KEY

@router.get('/', response_model=List[schema.HotelModel])
def all(db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    return db.query(HotelModel.Hotel).all()

@router.post('/new_hotel/', status_code=status.HTTP_201_CREATED)
def create(request: schema.HotelCreate, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    new_hotel = HotelModel.Hotel.create_hotel(db, request)
    db.refresh(new_hotel)
    return new_hotel

@router.put('/update_hotel/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schema.HotelCreate, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = HotelModel.Hotel.update_hotel(db, id, request)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {id} not found")
    return 'updated'

@router.delete('/delete_hotel/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = HotelModel.Hotel.delete_hotel(db, id)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {id} not found")
    return 'deleted'

@router.get('/find_hotel_id/{id}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def show(id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = HotelModel.Hotel.get_hotel_by_id(db, id)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {id} not found")
    return hotel

@router.get('/find_hotel_name/{name}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def search_hotels(name: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = HotelModel.Hotel.get_hotel_by_name(db, name)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with name {name} not found")
    return hotel

@router.get('/find_hotel_location/{location}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def search_hotels(location: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = HotelModel.Hotel.get_hotel_by_location(db, location)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with location {location} not found")
    return hotel

@router.get('/location_internal/{location}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def search_locations_internal(location: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    locations = HotelModel.Location.get_location_by_name(db, location)
    if locations == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with location {location} not found")
    return locations

@router.get('/location_external/{location}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def search_locations_external(location: str, db: Session = Depends(get_db)):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
    querystring = {"query":location}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with location {location} not found")
    
    locations = response.json()['data']
    locations_list = []
    print(locations[0])
    # Cache locations in database
    #cache_locations(locations_list, db) 

    return response.json()

@router.get('/hotel_internal/{locationID}/{checkInDate}/{checkOutDate}/{guests}/{rooms}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def search_hotels_internal(locationID: str, checkInDate: str, checkOutDate: str, guests: int, rooms: int, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotels = HotelModel.Hotel.get_hotel_by_request(locationID, checkInDate, checkOutDate, guests, rooms, db)
    if hotels == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with location {locationID} not found")
    return hotels

@router.get('/hotel_external/{locationID}/{checkInDate}/{checkOutDate}/{guests}/{rooms}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def search_hotels_external(locationID: str, checkInDate: str, checkOutDate: str, guests: int, rooms: int, db: Session = Depends(get_db)):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
    querystring = {
        "dest_id":locationID,
        "search_type":"CITY",
        "arrival_date":checkInDate,
        "departure_date":checkOutDate,
        "adults":guests,
        "room_qty":rooms,
        "currency_code":"USD",
    }
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "booking-com15.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with location {locationID} not found")
    
    hotels = response.json()['data']['hotels']
    hotels_list = []
    for hotel in hotels:
        hotels_list.append(schema.HotelCreate(
            name=hotel['property']['name'], 
            location=hotel['property']['wishlistName'],
            checkInDate=checkInDate,
            checkOutDate=checkOutDate,
            guests=guests,
            rooms=rooms,
            reviewScore=hotel['property']['reviewScore'],
            totalPrice=hotel['property']['priceBreakdown']['grossPrice']['value']
        ))
    # Cache hotels in database
    cache_hotels(hotels_list, db) 

    return response.json()




def cache_locations(locations: List[schema.LocationModel], db: Session):
        for location in locations:
            new_location = HotelModel.Location(
                name=location.name,
                geoId=location.geoId,
                type = "BookingAPI"
            )
            db.add(new_location)
        db.commit()



def cache_hotels(hotels: List[schema.HotelCreate], db: Session):
        for hotel in hotels:
            new_hotel = HotelModel.Hotel(
                name=hotel.name,
                location=hotel.location,
                checkInDate=hotel.checkInDate,
                checkOutDate=hotel.checkOutDate,
                guests=hotel.guests,
                rooms=hotel.rooms,
                reviewScore=hotel.reviewScore,
                totalPrice=hotel.totalPrice
            )
            db.add(new_hotel)
        db.commit()
