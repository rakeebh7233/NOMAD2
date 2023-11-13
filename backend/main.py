from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from config import settings
from routers import flight, hotel, flight_booking  
import http.client
import models
import http.client
import schema
import json

def create_tables():         
	models.Base.metadata.create_all(bind=engine)
        
def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    return app

app = start_application()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

app.include_router(flight.router)
app.include_router(hotel.router)
app.include_router(flight_booking.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tripadvisorFlights")
async def root():
    conn = http.client.HTTPSConnection("tripadvisor16.p.rapidapi.com")

    headers = {

    }

    conn.request("GET", "/api/v1/flights/searchFlights?sourceAirportCode=BOM&destinationAirportCode=DEL&date=%3CREQUIRED%3E&itineraryType=%3CREQUIRED%3E&sortOrder=%3CREQUIRED%3E&numAdults=1&numSeniors=0&classOfService=%3CREQUIRED%3E&pageNumber=1&currencyCode=USD", headers=headers)

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    json_obj = json.loads(data)

    return {"data": json_obj["data"]}

@app.get("/tripadvisorHotels")
async def root():
    conn = http.client.HTTPSConnection("tripadvisor16.p.rapidapi.com")

    headers = {

    }

    conn.request("GET", "/api/v1/hotels/searchLocation?query=Dhaka", headers=headers)

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    json_obj = json.loads(data)

    geoID = json_obj["data"][0]["geoId"]

    conn.request("GET", "/api/v1/hotels/searchHotels?geoId="+ str(geoID) + "&checkIn=2023-11-13&checkOut=2023-11-14&pageNumber=1&currencyCode=USD", headers=headers)

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    json_obj = json.loads(data)

    return {"data": json_obj["data"]["data"]}

@app.get("/tripadvisorRestaurants")
async def root():
    conn = http.client.HTTPSConnection("tripadvisor16.p.rapidapi.com")

    headers = {

    }

    conn.request("GET", "/api/v1/restaurant/searchRestaurants?locationId=304551", headers=headers)

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    json_obj = json.loads(data)

    return {"data": json_obj["data"]}


@app.post("/register")
async def register(user: schema.UserCreate, db: db_dependency):
    print("registering user")
    db_user = models.User.get_user_by_email(user.email_address, db)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return models.User.create_user(user,db)