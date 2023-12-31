from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from config import settings
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import HotelModel
from suggestions import recs
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
    new_hotel = HotelModel.Hotel.create_hotel(request, db)
    db.refresh(new_hotel)
    return new_hotel

@router.put('/update_hotel/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schema.HotelCreate, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = HotelModel.Hotel.update_hotel(id, request, db)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {id} not found")
    return 'updated'

@router.delete('/delete_hotel/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = HotelModel.Hotel.delete_hotel(id, db)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {id} not found")
    return 'deleted'

@router.get('/find_hotel_id/{id}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def show(id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = HotelModel.Hotel.get_hotel_by_id(id, db)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {id} not found")
    return hotel

@router.get('/find_hotel/name/{name}', status_code=status.HTTP_200_OK, response_model=schema.HotelModel)
def search_hotels(name: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotel = HotelModel.Hotel.get_hotel_by_name(name, db)
    if hotel == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with name {name} not found")
    return hotel

@router.get('/find_hotel/location/{location}', status_code=status.HTTP_200_OK, response_model=List[schema.HotelModel])
def search_hotels_location(location: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotels = HotelModel.Hotel.get_hotel_by_location(location, db)
    if hotels == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with location {location} not found")
    return hotels


@router.get('/location_internal/{location}', status_code=status.HTTP_200_OK)
# Will put back in after testing API Call: current_user: schema.UserModel = Depends(oauth2.get_current_user)
def search_locations_internal(location: str, db: Session = Depends(get_db)):
    locations = HotelModel.Location.get_location_by_name(db, location, "BookingAPI")
    if locations != None:
        return {'isInDB': True, 'geoId': locations.geoId}
    else:
        return {'isInDB': False}

@router.get('/location_external/{location}', status_code=status.HTTP_200_OK)
# Will put back in after testing API Call: current_user: schema.UserModel = Depends(oauth2.get_current_user)
def search_locations_external(location: str, db: Session = Depends(get_db)):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
    querystring = {"query":location}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    # if response.status_code != 200:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with location {location} not found")

    response1 = HotelModel.Location.get_location_by_name(db, location,"BookingAPI")
    
    if response.status_code == 200 and response1 == None:
        locations = response.json()['data'][0]
        location = schema.LocationModel(
            name=locations['city_name'],
            geoId=locations['dest_id'],
            type="BookingAPI"
        )
        # Cache locations in database
        cache_locations(location, db) 

        return location 

@router.get('/hotel_internal/{locationID}/{checkInDate}/{checkOutDate}/{guests}/{rooms}', status_code=status.HTTP_200_OK)
# Will put back in after testing API Call: current_user: schema.UserModel = Depends(oauth2.get_current_user)
def search_hotels_internal(locationID: str, checkInDate: str, checkOutDate: str, guests: int, rooms: int, db: Session = Depends(get_db)):
    location = HotelModel.Location.get_location_by_id(db, locationID, 'BookingAPI')
    hotels = HotelModel.Hotel.get_hotel_by_request(location.name, checkInDate, checkOutDate, guests, rooms, db)
    if hotels == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with location {locationID} not found")
    return hotels

@router.get('/hotel_internal/budget/{locationID}/{checkInDate}/{checkOutDate}/{guests}/{rooms}/{budget}', status_code=status.HTTP_200_OK, response_model=List[schema.HotelModel])
def search_hotels_internal_budget(locationID: str, checkInDate: str, checkOutDate: str, guests: int, rooms: int, budget: int, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    hotels = HotelModel.Hotel.get_hotel_by_budget(locationID, checkInDate, checkOutDate, guests, rooms, budget, db)
    if hotels == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with location {locationID} not found")
    return hotels

@router.get('/hotel_external/{locationID}/{checkInDate}/{checkOutDate}/{guests}/{rooms}', status_code=status.HTTP_200_OK)
# Will put back in after testing API Call: current_user: schema.UserModel = Depends(oauth2.get_current_user)
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
    print("Call Successful for Hotel API")
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
    print("Hotels from external API cached in database")

    #return response.json()
    return hotels_list




def cache_locations(location: schema.LocationModel, db: Session):
        new_location = HotelModel.Location(
            name=location.name,
            geoId=location.geoId,
            type = location.type
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


@router.get('/suggestions/{hotel_id}', status_code=status.HTTP_200_OK, response_model=List[schema.HotelModel])
def get_suggested_hotels(hotel_id: int, db: Session = Depends(get_db)):
    hotel = show(hotel_id, db)
    hotel_id = hotel.id
    recommended_hotels = recs.get_hotel_suggestions(hotel_id)
    # print("Recommended Hotels: ", recommended_hotels)
    suggested_hotels = []
    for hid in recommended_hotels:
        rec_hotel = show(int(hid+1), db)
        suggested_hotels.append(rec_hotel)
    return suggested_hotels
