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

@app.get("/tripadvisor")
async def root():
    conn = http.client.HTTPSConnection("tripadvisor16.p.rapidapi.com")

    headers = {
    }

    conn.request("GET", "/api/v1/flights/searchAirport?query=london", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return {"data": data}

@app.post("/register")
async def register(user: schema.UserCreate, db: db_dependency):
    print("registering user")
    db_user = models.User.get_user_by_email(user.email_address, db)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return models.User.create_user(user,db)