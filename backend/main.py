from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from config import settings
import http.client
import models
import http.client


def create_tables():         
	models.Base.metadata.create_all(bind=engine)
        
def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    return app

app = start_application()

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

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

