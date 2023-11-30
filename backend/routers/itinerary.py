from typing import List
from fastapi import APIRouter, Body, HTTPException
from importlib import import_module
from sqlalchemy import delete
from datetime import date
from models.ItineraryModel import Itinerary
from models.ItineraryModel import user_itinerary
from database import db_dependency
import schema
from models.FlightModel import FlightBooking
from models.HotelModel import HotelBooking

router = APIRouter(
    prefix = "/itineraries",
    tags = ['Itineraries']
)

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
        departure=itinerary.departure,
        departureDate=itinerary.departureDate,
        returnDate=itinerary.returnDate,
        travelReason=itinerary.travelReason,
        leisureActivites=itinerary.leisureActivites,
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
    itinerary_obj.departure = itinerary.departure
    itinerary_obj.departureDate = itinerary.departureDate
    itinerary_obj.returnDate = itinerary.returnDate
    itinerary_obj.travelReason = itinerary.travelReason
    itinerary_obj.leisureActivites = itinerary.leisureActivites
    itinerary_obj.budget = itinerary.budget
    itinerary_obj.creator = creator

    db.commit()

    return itinerary_obj

    # Note for later: user permissions to delete may need to be checked
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

@router.get("/price/flight/{itinerary_id}")
def get_flight_price(itinerary_id: int, db: db_dependency):
    itinerary = db.query(Itinerary).filter_by(id=itinerary_id).first()

    if not itinerary:
        #raise HTTPException(status_code=404, detail="Itinerary not found")
        return {"total_price": -1}

    flights = db.query(flight_booking).filter_by(itinerary_id=itinerary_id).all()

    total_price = 0
    for flight in flights:
        total_price += flight.price

    return {"total_price": total_price}

@router.get("/price/hotel/{itinerary_id}")
def get_hotel_price(itinerary_id: int, db: db_dependency):
    itinerary = db.query(Itinerary).filter_by(id=itinerary_id).first()

    if not itinerary:
        #raise HTTPException(status_code=404, detail="Itinerary not found")
        return {"total_price": -1}

    hotels = db.query(hotel_booking).filter_by(itinerary_id=itinerary_id).all()

    total_price = 0
    for hotel in hotels:
        total_price += hotel.price

    return {"total_price": total_price}
    