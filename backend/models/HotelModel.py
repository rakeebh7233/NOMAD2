from sqlalchemy import Column, Sequence, ForeignKey, String, Integer, Float, Date
from database import Base
import schema

class Hotel(Base):
    __tablename__ = 'hotel'

    id = Column(Integer, Sequence('hotel_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    reviewScore = Column(Float, nullable=False)

    def __repr__(self):
        return f'<Hotel {self.name}>'

    @classmethod
    def create_hotel(cls, hotel: schema.HotelCreate, db_session):
        """Create a new hotel."""
        hotel_obj = cls(
            name=hotel.name,
            location=hotel.location,
            reviewScore=hotel.reviewScore,
        )
        db_session.add(hotel_obj)
        db_session.commit()
        return hotel_obj

    @classmethod
    def get_all_hotels(cls, db_session):
        return db_session.query(cls).all()

    @classmethod
    def get_hotel_by_id(cls, hotel_id, db_session):
        return db_session.query(cls).filter_by(id=hotel_id).first()

    @classmethod
    def get_hotel_by_name(cls, name, db_session):
        return db_session.query(cls).filter_by(name=name)
    
    @classmethod
    def get_hotel_by_location(cls, location, db_session):
        return db_session.query(cls).filter_by(location=location)

    @classmethod
    def update_hotel(cls, hotel_id, hotel: schema.HotelUpdate, db_session):
        """Update an existing flight."""
        hotel_obj = db_session.query(cls).filter_by(hotel_id=hotel_id).first()
        if hotel_obj:
            hotel_obj.name = hotel.name
            hotel_obj.location = hotel.location
            hotel_obj.reviewScore = hotel.reviewScore
            return hotel_obj
        else:
            return None


class HotelBooking(Base):
    __tablename__ = 'hotel_booking'

    hotel_id = Column(Integer, ForeignKey('hotel.id'), primary_key=True)
    itinerary_id = Column(Integer, ForeignKey(
        'itinerary.id'), primary_key=True)
    checkInDate = Column(Date, nullable=False)
    checkOutDate = Column(Date, nullable=False)
    guests = Column(Integer, nullable=False)
    rooms = Column(Integer, nullable=False)
    totalPrice = Column(Float, nullable=False)

    def __repr__(self):
        return f'<HotelBooking {self.hotel_id} {self.itinerary_id_id}>'

    @classmethod
    def create_hotel_booking(cls, hotel_booking: schema.HotelBookingCreate, db_session):
        """Create a new hotel booking."""
        hotel_booking_obj = cls(
            hotel_id=hotel_booking.hotel_id,
            itinerary_id=hotel_booking.itinerary_id,
            checkInDate=hotel_booking.checkInDate,
            checkOutDate=hotel_booking.checkOutDate,
            guests=hotel_booking.guests,
            rooms=hotel_booking.rooms,
            totalPrice=hotel_booking.totalPrice,
        )
        db_session.add(hotel_booking_obj)
        db_session.commit()
        return hotel_booking_obj

    @classmethod
    def get_hotel_booking(cls, hotel_id, itinerary_id, db_session):
        """Get a hotel booking by hotel_id and user_id."""
        return db_session.query(cls).filter_by(hotel_id=hotel_id, itinerary_id_id=itinerary_id).first()

    @classmethod
    def get_all_hotel_bookings(cls, db_session):
        """Get all hotel bookings."""
        return db_session.query(cls).all()

    @classmethod
    def get_hotel_booking_by_itinerary_id(cls, itinerary_id, db_session):
        """Get all hotel bookings by user_id."""
        return db_session.query(cls).filter_by(itinerary_id=itinerary_id).all()

    @classmethod
    def update_hotel_booking(cls, hotel_id, itinerary_id, hotel_booking: schema.HotelBookingUpdate, db_session):
        """Update an existing hotel booking."""
        hotel_booking_obj = db_session.query(cls).filter_by(
            hotel_id=hotel_id, itinerary_id=itinerary_id).first()
        if hotel_booking_obj:
            hotel_booking_obj.checkInDate = hotel_booking.checkInDate
            hotel_booking_obj.checkOutDate = hotel_booking.checkOutDate
            hotel_booking_obj.guests = hotel_booking.guests
            hotel_booking_obj.rooms = hotel_booking.rooms
            hotel_booking_obj.totalPrice = hotel_booking.totalPrice
            db_session.commit()
            return hotel_booking_obj
        else:
            return None

    @classmethod
    def delete_hotel_booking(cls, hotel_id, itinerary_id, db_session):
        """Delete an existing hotel booking."""
        hotel_booking_obj = db_session.query(cls).filter_by(
            hotel_id=hotel_id, itinerary_id=itinerary_id).first()
        if hotel_booking_obj:
            db_session.delete(hotel_booking_obj)
            db_session.commit()
            return hotel_booking_obj
        else:
            return None