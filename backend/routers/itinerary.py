from fastapi import APIRouter, HTTPException
from importlib import import_module
from models import ItineraryModel
from database import db_dependency
import schema

router = APIRouter(
    prefix = "/itinerary",
    tags = ['Itineraries']
)

@router.post("/create")
def create_itinerary(itinerary: schema.ItineraryCreate, db: db_dependency):
    print("creating itinerary")
    User = import_module("models.UserModel").User

    members = []
    if itinerary.emailList:
        members = db.query(User).filter(User.email_address.in_(itinerary.emailList)).all()

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
        creator_id=itinerary.creator_id,
    )

    # Add the fetched users to the members relationship
    for member in members:
        itinerary_obj.members.append(member)

    db.add(itinerary_obj)
    db.commit()
    db.refresh(itinerary_obj)
    return itinerary_obj
    