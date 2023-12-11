from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import RestaurantModel, HotelModel
from sqlalchemy.orm import Session
import requests 
from config import settings

router = APIRouter(
    prefix = "/restaurant",
    tags = ['Restaurants']
)

get_db = database.get_db

API_KEY = settings.API_KEY

@router.get('/tripadvisorSearch/{locId}', status_code=status.HTTP_200_OK)
def search_restaurants_external(locId: str, db: Session = Depends(get_db)):

    url = "https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchRestaurants"

    querystring = {"locationId": locId}

    headers = {
        'X-RapidAPI-Key': API_KEY,
        'X-RapidAPI-Host': 'tripadvisor16.p.rapidapi.com'
    }

    restaurantList = []

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurants with locationId {locId} not found")
    theResponse = response.json()
    for rest in theResponse["data"]["data"]:
        restaurantList.append({"locationId": locId, "name": rest["name"], "averageRating": rest["averageRating"], "userReviewCount": rest["userReviewCount"], "priceTag": rest["priceTag"], "menuUrl": rest["menuUrl"]})
        restSchema = schema.RestaurantBase(
            locationId = locId,
            name = rest["name"],
            averageRating = rest["averageRating"],
            userReviewCount = rest["userReviewCount"],
            priceTag = rest["priceTag"],
            menuURL = rest["menuUrl"]
        )
        RestaurantModel.Restaurant.create_restaurant(restSchema, db)
    return restaurantList

@router.get('/tripadvisorRestaurantLocCheck/{locationId}', status_code=status.HTTP_200_OK)
def checkLocExists(locId: str, db: Session = Depends(get_db)):

    res = RestaurantModel.Restaurant.checkLocationID(locId, db)

    if res != None:
        return {'isInDB': True}
    else:
        return {'isInDB': False}

@router.get('/{locId}', response_model=List[schema.RestaurantModel])
def all(locId: str, db: Session = Depends(get_db)):
    return db.query(RestaurantModel.Restaurant).filter_by(locationId = locId).all()

@router.get('/locations/{city}')
def newlocationSearchExternal(city: str, db: Session = Depends(get_db)):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation"

    querystring = {"query": city}

    headers = {
        'X-RapidAPI-Key': API_KEY,
        'X-RapidAPI-Host': 'tripadvisor16.p.rapidapi.com'
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    # if response.status_code != 200:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{city} not found!")
    
    if response.status_code == 200:
        theResponse = response.json()

        restSchema = schema.LocationBase(
                name = city,
                geoId = theResponse['data'][0]['geoId'],
                type = 'TripAdvisorAPI'
        )
        
        HotelModel.Location.create_location(restSchema, db)

        return {"geoId" :theResponse['data'][0]['geoId']}

@router.get('/tripadvisorCityCheck/{city}', status_code=status.HTTP_200_OK)
def checkLocExists(city: str, db: Session = Depends(get_db)):

    print("This is the city: " + city)

    res = HotelModel.Location.get_location_by_name(db, city, "TripAdvisorAPI")
    
    if res != None:
        return {'isInDB': True, 'geoID': res.geoId}
    else:
        return {'isInDB': False}