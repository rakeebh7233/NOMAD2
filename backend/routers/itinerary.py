from typing import List
from fastapi import APIRouter, HTTPException
from importlib import import_module
from models import ItineraryModel
from database import db_dependency
import schema

router = APIRouter(
    prefix = "/itinerary",
    tags = ['Itineraries']
)

@router.get("/{user_id}", response_model=List[schema.ItineraryModel])
def get_user_itineraries(user_id: int, db: db_dependency):
    User = import_module("models.UserModel").User
    itineraries = db.query(ItineraryModel.Itinerary).filter((ItineraryModel.Itinerary.creator_id == user_id) 
                                                            | (User.id.in_(ItineraryModel.Itinerary.members))).all()
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
    if itinerary.emailList:
        members = db.query(User).filter(User.email_address.in_(itinerary.emailList)).all()
        print(members)

        if len(members) != len(itinerary.emailList):
            raise HTTPException(status_code=400, detail="One or more emails are not registered")

    itinerary_obj = ItineraryModel.Itinerary(
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
    