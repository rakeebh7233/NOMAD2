from sqlalchemy import Column, Sequence, ForeignKey, String, Integer
from database import Base
import schema
# from .FlightModel import Flight
# from .HotelModel import Hotel


class Itinerary(Base):
    __tablename__ = 'itinerary'

    id = Column(Integer, Sequence('itinerary_id_seq'), primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey('flight.id'), nullable=False)
    hotel_id = Column(Integer, ForeignKey('hotel.id'), nullable=False)
    destination = Column(String, nullable=False)

    def __repr__(self):
        return f'<Itinerary {self.id}>'

    @classmethod
    def create_itinerary(cls, itinerary: schema.ItineraryCreate, db_session):
        """Create a new itinerary."""
        itinerary_obj = cls(
            flight_id=itinerary.flight_id,
            hotel_id=itinerary.hotel_id,
            destination=itinerary.destination,
        )
        db_session.add(itinerary_obj)
        db_session.commit()
        return itinerary_obj

    @classmethod
    def get_all_itineraries(cls, db_session):
        return db_session.query(cls).all()

    @classmethod
    def get_itinerary_by_id(cls, itinerary_id, db_session):
        return db_session.query(cls).filter_by(id=itinerary_id).first()

    @classmethod
    def update_itinerary(cls, itinerary_id, itinerary: schema.ItineraryUpdate, db_session):
        """Update an existing itinerary."""
        itinerary_obj = db_session.query(
            cls).filter_by(id=itinerary_id).first()
        if itinerary_obj:
            itinerary_obj.flight_id = itinerary.flight_id
            itinerary_obj.hotel_id = itinerary.hotel_id
            itinerary_obj.destination = itinerary.destination
            db_session.commit()
            return itinerary_obj
        else:
            return None

# class ItineraryOwner(Base):
#     __tablename__ = 'itinerary_owner'

#     itinerary_id = Column(Integer, ForeignKey('itinerary.id'), primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

#     def __repr__(self):
#         return f'<ItineraryOwner {self.itinerary_id} {self.user_id}>'

#     @classmethod
#     def create_itinerary_owner(cls, itinerary_owner: schema.ItineraryOwnerCreate, db_session):
#         """Create a new itinerary owner."""
#         itinerary_owner_obj = cls(
#             itinerary_id=itinerary_owner.itinerary_id,
#             user_id=itinerary_owner.user_id,
#         )
#         db_session.add(itinerary_owner_obj)
#         db_session.commit()
#         return itinerary_owner_obj

#     @classmethod
#     def get_itinerary_owner(cls, itinerary_id, user_id, db_session):
#         """Get an itinerary owner by itinerary_id and user_id."""
#         return db_session.query(cls).filter_by(itinerary_id=itinerary_id, user_id=user_id).first()

#     @classmethod
#     def get_all_itinerary_owners(cls, db_session):
#         """Get all itinerary owners."""
#         return db_session.query(cls).all()

#     @classmethod
#     def get_itinerary_by_user_id(cls, user_id, db_session):
#         """Get all itineraries by user_id."""
#         return db_session.query(cls).filter_by(user_id=user_id).all()

#     @classmethod
#     def update_itinerary_owner(cls, itinerary_id, user_id, itinerary_owner: schema.ItineraryOwnerUpdate, db_session):
#         """Update an existing itinerary owner."""
#         itinerary_owner_obj = db_session.query(cls).filter_by(itinerary_id=itinerary_id, user_id=user_id).first()
#         if itinerary_owner_obj:
#             itinerary_owner_obj.itinerary_id = itinerary_owner.itinerary_id
#             itinerary_owner_obj.user_id = itinerary_owner.user_id
#             db_session.commit()
#             return itinerary_owner_obj
#         else:
#             return None

#     @classmethod
#     def delete_itinerary_owner(cls, itinerary_id, user_id, db_session):
#         """Delete an existing itinerary owner."""
#         itinerary_owner_obj = db_session.query(cls).filter_by(itinerary_id=itinerary_id, user_id=user_id).first()
#         if itinerary_owner_obj:
#             db_session.delete(itinerary_owner_obj)
#             db_session.commit()
#             return itinerary_owner_obj
#         else:
#             return None