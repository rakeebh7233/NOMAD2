from typing import List
from fastapi import APIRouter, Body, HTTPException
from importlib import import_module
from sqlalchemy import delete
from sqlalchemy.orm import joinedload
from datetime import date
from models.ItineraryModel import Itinerary, user_itinerary
from models.ItineraryModel import user_itinerary
from models.FlightModel import FlightBooking
from models.HotelModel import HotelBooking
from models.RestaurantModel import RestaurantBooking, Restaurant
from database import db_dependency
import schema

router = APIRouter(
    prefix="/itineraries",
    tags=['Itineraries']
)

@router.get("/currItin/{itinerary_id}", response_model = List[schema.ViewItinerary])
def get_itinerary_byID(itin_id: int, db: db_dependency):
    itin = db.query(Itinerary).filter_by(id = itin_id).all()
    return itin

@router.get("/{user_id}", response_model=List[schema.ViewItinerary])
def get_user_itineraries(user_id: int, db: db_dependency):
    User = import_module("models.UserModel").User
    itineraries = db.query(Itinerary).filter((Itinerary.creator_id == user_id) 
            | (Itinerary.members.any(User.id == user_id))).filter(Itinerary.returnDate >= date.today()).all()
    if not itineraries:
        raise HTTPException(status_code=404, detail="No itineraries found for this user")
    
    # Fetch the creator's name for each itinerary and create a new dictionary
    itinerary_dicts = []
    for itinerary in itineraries:
        creator = db.query(User).filter_by(id=itinerary.creator_id).first()
        itinerary_dict = {c.name: getattr(itinerary, c.name) for c in itinerary.__table__.columns}
        itinerary_dict["creatorUsername"] = creator.username if creator else None
        itinerary_dict["members"] = [member for member in itinerary.members]  # Add this line
        itinerary_dicts.append(itinerary_dict)

    return itinerary_dicts

@router.get("/{user_id}/past", response_model=List[schema.ViewItinerary])
def get_user_itineraries(user_id: int, db: db_dependency):
    User = import_module("models.UserModel").User
    itineraries = db.query(Itinerary).filter((Itinerary.creator_id == user_id) 
            | (Itinerary.members.any(User.id == user_id))).filter(Itinerary.returnDate < date.today()).all()
    if not itineraries:
        raise HTTPException(status_code=404, detail="No itineraries found for this user")
    
    # Fetch the creator's name for each itinerary and create a new dictionary
    itinerary_dicts = []
    for itinerary in itineraries:
        creator = db.query(User).filter_by(id=itinerary.creator_id).first()
        itinerary_dict = {c.name: getattr(itinerary, c.name) for c in itinerary.__table__.columns}
        itinerary_dict["creatorUsername"] = creator.username if creator else None
        itinerary_dict["members"] = [member for member in itinerary.members]  # Add this line
        itinerary_dicts.append(itinerary_dict)

    return itinerary_dicts

@router.get("/{email}", response_model=List[schema.ItineraryModel])
def get_user_itineraries_by_email(email: str, db: db_dependency):
    User = import_module("models.UserModel").User
    user = db.query(User).filter_by(email_address=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    itineraries = db.query(Itinerary).filter((Itinerary.creator_id == user.id) 
                                                            | (Itinerary.members.any(User.id == user.id))).all()
    if not itineraries:
        raise HTTPException(status_code=404, detail="No itineraries found for this user")
    return itineraries

@router.post("/create")
def create_itinerary(itinerary: schema.ItineraryCreate, db: db_dependency):
    print("creating itinerary")
    User = import_module("models.UserModel").User

    # Fetch the creator
    creator = db.query(User).filter_by(id=itinerary.creator_id).first()

    members = []
    if itinerary.members:
        members = db.query(User).filter(User.email_address.in_(itinerary.members)).all()
        print(members)

        if len(members) != len(itinerary.members):
            raise HTTPException(status_code=400, detail="One or more emails are not registered")

    itinerary_obj = Itinerary(
        itineraryTitle=itinerary.itineraryTitle,
        destination=itinerary.destination,
        departureAirport=itinerary.departureAirport,
        arrivalAirport=itinerary.arrivalAirport,
        departureDate=itinerary.departureDate,
        returnDate=itinerary.returnDate,
        budget=itinerary.budget,
        creator=creator
    )

    # Add the fetched users to the members relationship
    for member in members:
        itinerary_obj.members.append(member)

    db.add(itinerary_obj)
    db.commit()
    db.refresh(itinerary_obj)
    return itinerary_obj

@router.put("/{itinerary_id}", response_model=schema.ItineraryModel)
def update_itinerary(itinerary_id: int, itinerary: schema.ItineraryCreate, db: db_dependency):
    User = import_module("models.UserModel").User

    # Fetch the itinerary
    itinerary_obj = db.query(Itinerary).filter_by(id=itinerary_id).first()

    if not itinerary_obj:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    # Fetch the creator
    creator = db.query(User).filter_by(id=itinerary.creator_id).first()
    
    members = []
    if itinerary.members:
        members = db.query(User).filter(User.email_address.in_(itinerary.members)).all()

        if len(members) != len(itinerary.members):
            raise HTTPException(status_code=400, detail="One or more emails are not registered")

    # Update the itinerary
    itinerary_obj.itineraryTitle = itinerary.itineraryTitle
    itinerary_obj.destination = itinerary.destination
    itinerary_obj.departureAirport = itinerary.departureAirport
    itinerary_obj.arrivalAirport = itinerary.arrivalAirport
    itinerary_obj.departureDate = itinerary.departureDate
    itinerary_obj.returnDate = itinerary.returnDate
    itinerary_obj.budget = itinerary.budget
    itinerary_obj.creator = creator

    # Add the fetched users to the members relationship
    for member in members:
        itinerary_obj.members.append(member)

    db.commit()

    return itinerary_obj

@router.delete("/{itinerary_id}")
def delete_itinerary(itinerary_id: int, db: db_dependency):
    # Fetch the itinerary
    itinerary = db.query(Itinerary).filter_by(id=itinerary_id).first()

    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    # Delete the associations
    stmt = delete(user_itinerary).where(user_itinerary.c.itinerary_id == itinerary_id)
    db.execute(stmt)

    # Delete the itinerary
    db.delete(itinerary)
    db.commit()

    return {"message": "Itinerary deleted successfully"}

@router.post("/{itinerary_id}/rating")
def rate_itinerary(db: db_dependency, itinerary_id: int, rating = Body(...)):
    itinerary = db.query(Itinerary).filter_by(id=itinerary_id).first()

    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    itinerary.rating = rating['rating']
    db.commit()
    db.refresh(itinerary)

    return itinerary

@router.get("/{itinerary_id}/restaurants")
def get_restaurants(itinerary_id: int, db: db_dependency):
    itinerary = db.query(Itinerary).filter_by(id=itinerary_id).first()

    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    restaurants = db.query(RestaurantBooking).options(joinedload(RestaurantBooking.restaurant)).filter_by(itinerary_id=itinerary_id).all()

    return restaurants

@router.get("/{itinerary_id}/flights")
def get_flights(itinerary_id: int, db: db_dependency):
    itinerary = db.query(Itinerary).filter_by(id=itinerary_id).first()

    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    flights = db.query(FlightBooking).options(joinedload(FlightBooking.flight)).filter_by(itinerary_id=itinerary_id).all()

    return flights

@router.get("/{itinerary_id}/hotels")
def get_hotels(itinerary_id: int, db: db_dependency):
    itinerary = db.query(Itinerary).filter_by(id=itinerary_id).first()

    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    hotels = db.query(HotelBooking).options(joinedload(HotelBooking.hotel)).filter_by(itinerary_id=itinerary_id).all()

    return hotels

@router.get("/price/total/{itinerary_id}")
def get_total_price(itinerary_id: int, db: db_dependency):
    itinerary = db.query(Itinerary).filter_by(id=itinerary_id).first()

    if not itinerary:
        #raise HTTPException(status_code=404, detail="Itinerary not found")
        return {"total_price": -1}

    flights = db.query(FlightBooking).filter_by(itinerary_id=itinerary_id).all()
    hotels = db.query(HotelBooking).filter_by(itinerary_id=itinerary_id).all()

    total_price = 0
    for flight in flights:
        total_price += flight.price

    for hotel in hotels:
        total_price += hotel.price

    return {"total_price": total_price}


@router.get("/next_trip/date/{email_address}")
def get_next_trip_date(email_address: str, db: db_dependency):
    earliest_departure_date = Itinerary.get_earliest_departure_date(email_address, db)  
    if earliest_departure_date == -1:
        return {"earliest_departure_date": -1}
    return {"earliest_departure_date": earliest_departure_date}

@router.get("/next_trip/itinerary/{email_address}/{departure_date}")
def get_next_trip_itinerary(email_address: str, departure_date: date, db: db_dependency):
    itinerary_id = Itinerary.get_itinerary_by_email_and_departure_date(email_address, departure_date, db)
    if itinerary_id == None:
        return {"itinerary_id": -1}
    return {"itinerary_id": itinerary_id}

@router.get("/next_trip/price/{itinerary_id}")
def get_next_trip_price(itinerary_id: int, db: db_dependency):
    price = Itinerary.get_itinerary_price(itinerary_id, db)
    return {"price": price}


    
    