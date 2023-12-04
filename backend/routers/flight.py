from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from config import settings
import sys 
sys.path.append("..")
import schema, database, oauth2
from models import FlightModel
from suggestions import recs
from sqlalchemy.orm import Session
import requests


router = APIRouter(
    prefix="/flight",
    tags=['Flights']
)

get_db = database.get_db

API_KEY = settings.API_KEY

# Add this back into function parameters after testing the API calls 
# current_user: schema.UserModel = Depends(oauth2.get_current_user)

@router.get('/', response_model=List[schema.FlightModel])
def all(db: Session = Depends(get_db)):
    return db.query(FlightModel.Flight).all()

@router.post('/new_flight/', status_code=status.HTTP_201_CREATED)
def create(request: schema.FlightCreate, db: Session = Depends(get_db)):
    new_flight = FlightModel.Flight.create_flight(request, db)
    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)
    return new_flight

@router.put('/update_flight/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schema.FlightUpdate, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FlightModel.Flight.update_flight(id, request, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with id {id} not found")
    return 'updated'

@router.delete('/delete_flight/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FlightModel.Flight.delete_flight(id, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with id {id} not found")
    return 'deleted'

@router.get('/find_flight_id/{id}', status_code=status.HTTP_200_OK, response_model=schema.FlightModel)
# current_user: schema.UserModel = Depends(oauth2.get_current_user)
def show(id, db: Session = Depends(get_db)):
    response = FlightModel.Flight.get_flight_by_id(id, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with id {id} not found")
    return response

@router.get('/internal_search/round/{departureAirport}/{arrivalAirport}/{departureTime}/{arrivalTime}/{search}', status_code=status.HTTP_200_OK, response_model=List[schema.FlightModel])
def search_flights_int(departureAirport: str, arrivalAirport: str, departureTime: str, arrivalTime: str, cabinClass: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FlightModel.Flight.get_flight_by_request(departureAirport, arrivalAirport, departureTime, arrivalTime, cabinClass, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to retrieve flights")
    return response

@router.get('internal_search/round/budeget/{departureAirport}/{arrivalAirport}/{departureTime}/{arrivalTime}/{budget}', status_code=status.HTTP_200_OK, response_model=List[schema.FlightModel])
def search_flights_int_budget(departureAirport: str, arrivalAirport: str, departureTime: str, arrivalTime: str, budget: int, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FlightModel.Flight.get_flight_by_price(departureAirport, arrivalAirport, departureTime, arrivalTime, budget, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to retrieve flights")
    return response

@router.get('/internal_search/oneway/{departureAirport}/{arrivalAirport}/{departureTime}/{cabinClass}', status_code=status.HTTP_200_OK, response_model=List[schema.FlightModel])
def search_flights_int_oneway(departureAirport: str, arrivalAirport: str, departureTime: str, cabinClass: str, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FlightModel.Flight.get_flight_oneway(departureAirport, arrivalAirport, departureTime, cabinClass, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to retrieve flights")
    return response

@router.get('/internal_search/oneway/budget/{departureAirport}/{arrivalAirport}/{departureTime}/{budget}', status_code=status.HTTP_200_OK, response_model=List[schema.FlightModel])
def search_flights_int_oneway_budget(departureAirport: str, arrivalAirport: str, departureTime: str, budget: int, db: Session = Depends(get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    response = FlightModel.Flight.get_flight_by_oneway_price(departureAirport, arrivalAirport, departureTime, budget, db)
    if response == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to retrieve flights")
    return response

@router.get('/external_search/round/{departureAirport}/{arrivalAirport}/{departureTime}/{arrivalTime}/{cabinClass}', status_code=status.HTTP_200_OK, response_model=List[schema.FlightCreate])
def search_flights_ext(departureAirport: str, arrivalAirport: str, departureTime: str, arrivalTime: str, cabinClass: str, db: Session = Depends(get_db)):
    
    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"
    querystring = {"fromId":departureAirport + ".AIRPORT",
                "toId":arrivalAirport + ".AIRPORT",
                "departDate":departureTime,
                "returnDate":arrivalTime,
                "cabinClass":cabinClass,
                "sort":"BEST",
                "currency_code":"USD"}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    response = requests.request('GET', url, headers=headers, params=querystring)

    if response.status_code != 200:
        print("Call Failed for Flights API")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve flights")
    print("Call Successful for Flights API")
    #Cachine Flights in Database
    flights = response.json()['data']['flightOffers']
    flights_list = []
    for flight in flights:
        for i in range(len(flight['segments'])):
            flight_model = schema.FlightCreate(
                departureAirport=flight['segments'][i]['departureAirport']['code'],
                arrivalAirport=flight['segments'][i]['arrivalAirport']['code'],
                departureTime=flight['segments'][i]['departureTime'][0:10],
                arrivalTime=flight['segments'][i]['arrivalTime'][0:10],
                cabinClass=flight['segments'][i]['legs'][0]['cabinClass'],
                carrier=flight['segments'][i]['legs'][0]['carriersData'][0]['name'],
                totalPrice=flight['priceBreakdown']['total']['units']
            )
            flights_list.append(flight_model)
    print(flights_list)
    cache_flights(flights_list, db)
    print("Flights from external API cached in database")
    # return response.json()
    return flights_list

@router.get('/external_search/oneway/{departureAirport}/{arrivalAirport}/{departureTime}/{cabinClass}', status_code=status.HTTP_200_OK, response_model=List[schema.FlightCreate])
def search_flights_ext_oneway(departureAirport: str, arrivalAirport: str, departureTime: str, cabinClass: str, db: Session = Depends(get_db)):
    
    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"
    querystring = {"fromId":departureAirport + ".AIRPORT",
                "toId":arrivalAirport + ".AIRPORT",
                "departDate":departureTime,
                "cabinClass":cabinClass,
                "sort":"BEST",
                "currency_code":"USD"}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    response = requests.request('GET', url, headers=headers, params=querystring)

    if response.status_code != 200:
        print("Call Failed for Flights API")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve flights")
    print("Call Successful for Flights API")
    #Cachine Flights in Database
    flights = response.json()['data']['flightOffers']
    flights_list = []
    for flight in flights:
        for i in range(len(flight['segments'])):
            flight_model = schema.FlightCreate(
                departureAirport=flight['segments'][i]['departureAirport']['code'],
                arrivalAirport=flight['segments'][i]['arrivalAirport']['code'],
                departureTime=flight['segments'][i]['departureTime'][0:10],
                arrivalTime=flight['segments'][i]['arrivalTime'][0:10],
                cabinClass=flight['segments'][i]['legs'][0]['cabinClass'],
                carrier=flight['segments'][i]['legs'][0]['carriersData'][0]['name'],
                totalPrice=flight['priceBreakdown']['total']['units']
            )
            flights_list.append(flight_model)
    print(flights_list)
    cache_flights(flights_list, db)
    print("Flights from external API cached in database")
    # print(response.json())
    # return response.json()
    return flights_list

@router.get('/isInDB/')

def cache_flights(flights: List[schema.FlightCreate], db: Session = Depends(get_db)):
    for flight in flights:
        # new_flight = 
        FlightModel.Flight.create_flight(flight, db)
        "Flight Created"
        # db.add(new_flight)
        # db.commit()
        # db.refresh(new_flight)
    # return flights

# @router.get('suggestions/{flight_id}', status_code=status.HTTP_200_OK, response_model=int)
# def get_suggested_flights(flight_id: int, db: Session = Depends(get_db)):
#     flight = show(flight_id, db)
#     # suggestions = Suggestions()
#     recommended_flights = Suggestions.generate_flight_recommendations(flight)
#     print("Recommended Flightds: ", round(recommended_flights[0]))
#     return round(recommended_flights[0])


#Select flight to get recommendations for based on the flight id
#Uses a cosine similarity scheme to find similar flights
@router.get('/suggestions/{flight_id}', status_code=status.HTTP_200_OK, response_model=List[schema.FlightModel])
def get_suggested_flights(flight_id: int, db: Session = Depends(get_db)):
    flight = show(flight_id, db)
    flight_id = flight.id
    recommended_flights = recs.get_flight_suggestions(flight_id)
    # print("Recommended Flightds: ", recommended_flights)
    suggested_flights = []
    for fid in recommended_flights:
        rec_flight = show(int(fid+1), db)
        suggested_flights.append(rec_flight)
    return suggested_flights

