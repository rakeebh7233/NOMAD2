from fastapi import APIRouter
import http
import json

router = APIRouter()


@router.get("/tripadvisorFlights")
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

    # return {"data": json_obj["data"]["data"]}
    return {"data": json_obj["data"]["data"]}



@router.get("/tripadvisorRestaurants")
def get_restaurants():
    conn = http.client.HTTPSConnection("tripadvisor16.p.rapidapi.com")

    headers = {

    }

    conn.request(
        "GET", "/api/v1/restaurant/searchRestaurants?locationId=304551", headers=headers)

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    json_obj = json.loads(data)

    return {"data": json_obj["data"]}
