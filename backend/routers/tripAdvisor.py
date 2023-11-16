from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import RestaurantModel
from sqlalchemy.orm import Session
import requests 

router = APIRouter(
    prefix = "/restaurant",
    tags = ['Restaurants']
)

get_db = database.get_db

API_KEY = "xxx"

""" @router.get("/tripadvisorFlights")
def get_flights():
    conn = http.client.HTTPSConnection("tripadvisor16.p.rapidapi.com")

    headers = {

    }

    conn.request("GET", "/api/v1/flights/searchFlights?sourceAirportCode=BOM&destinationAirportCode=DEL&date=%3CREQUIRED%3E&itineraryType=%3CREQUIRED%3E&sortOrder=%3CREQUIRED%3E&numAdults=1&numSeniors=0&classOfService=%3CREQUIRED%3E&pageNumber=1&currencyCode=USD", headers=headers)

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    json_obj = json.loads(data)

    return {"data": json_obj["data"]}


@router.get("/tripadvisorHotels")
def get_hotels():
    conn = http.client.HTTPSConnection("tripadvisor16.p.rapidapi.com")

    headers = {

    }

    conn.request(
        "GET", "/api/v1/hotels/searchLocation?query=Dhaka", headers=headers)

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    json_obj = json.loads(data)

    geoID = json_obj["data"][0]["geoId"]

    conn.request("GET", "/api/v1/hotels/searchHotels?geoId=" + str(geoID) +
                 "&checkIn=2023-11-13&checkOut=2023-11-14&pageNumber=1&currencyCode=USD", headers=headers)

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    json_obj = json.loads(data)

    return {"data": json_obj["data"]["data"]} """


@router.get('/tripadvisorSearch/{locationId}', status_code=status.HTTP_200_OK)
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurants with locationId {locationId} not found")
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
