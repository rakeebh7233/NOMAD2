from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from config import settings
from sqlalchemy.orm import Session
from routers import user, flight, hotel, flight_booking, hotel_booking, tripAdvisor, personal_finance, personal_savings, itinerary, restaurant_booking
from database import Base
from suggestions import Suggestions
import os.path
import database

get_db = database.get_db


def create_tables():         
	Base.metadata.create_all(bind=engine)

        
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

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user.router)
app.include_router(itinerary.router)
app.include_router(personal_finance.router)
app.include_router(personal_savings.router)
app.include_router(tripAdvisor.router)
app.include_router(flight.router)
app.include_router(hotel.router)
app.include_router(flight_booking.router)
app.include_router(hotel_booking.router)
app.include_router(restaurant_booking.router)



