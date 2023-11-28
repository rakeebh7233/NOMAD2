from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from config import settings
from routers import user, flight, hotel, flight_booking, hotel_booking, tripAdvisor, personal_finance, personal_savings, itinerary, restaurant_booking
from database import Base
from suggestions import Suggestions


def create_tables():         
	Base.metadata.create_all(bind=engine)
     
def train_flight_suggestions():
    suggestions = Suggestions()
    flights = suggestions.load_flight_data()
    training_data, test_data = suggestions.prepare_flight_data(flights)
    suggestions.train_recommender_system(training_data, test_data, 100, 'flight')

def train_hotel_suggestions():
    suggestions = Suggestions()
    hotels = suggestions.load_hotel_data()
    training_data, test_data = suggestions.prepare_hotel_data(hotels)
    suggestions.train_recommender_system(training_data, test_data, 100, 'hotel')

        
def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    #train_flight_suggestions()
    #train_hotel_suggestions()
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
app.include_router(restaurant_booking)



