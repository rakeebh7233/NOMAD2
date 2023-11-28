from sqlalchemy import Column, Sequence, ForeignKey, String, Integer, Float, Date
from database import Base
import schema

class Location(Base):
    __tablename__ = 'location'

    name = Column(String, primary_key=True)
    geoId = Column(Integer, nullable=False)
    type = Column(String, nullable=False)

    def __repr__(self):
        return f'<Location {self.name}>'
    
    @classmethod
    def create_location(cls, location: schema.LocationCreate, db_session):
        """Create a new location."""
        location_obj = cls(
            name=location.name,
            geoId=location.geoId,
            type = location.type
        )
        db_session.add(location_obj)
        db_session.commit()
        return location_obj
    
    @classmethod
    def get_all_locations(cls, db_session):
        return db_session.query(cls).all()
    
    @classmethod
    def get_location_by_name(cls, name, db_session):
        return db_session.query(cls).filter_by(name=name).first()
    
    @classmethod
    def checkifCityExistsinDB(cls, city, db_session):
        return db_session.query(cls).filter_by(name = city).first()

class Hotel(Base):
    __tablename__ = 'hotel'

    id = Column(Integer, Sequence('hotel_id_seq'), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    checkInDate = Column(Date, nullable=False)
    checkOutDate = Column(Date, nullable=False)
    guests = Column(Integer, nullable=False)
    rooms = Column(Integer, nullable=False)
    reviewScore = Column(Float, nullable=False)
    totalPrice = Column(Float, nullable=False)

    def __repr__(self):
        return f'<Hotel {self.name}>'

    @classmethod
    def create_hotel(cls, hotel: schema.HotelCreate, db_session):
        """Create a new hotel."""
        hotel_obj = cls(
            name=hotel.name,
            location=hotel.location,
            checkInDate=hotel.checkInDate,
            checkOutDate=hotel.checkOutDate,
            guests=hotel.guests,
            rooms=hotel.rooms,
            reviewScore=hotel.reviewScore,
            totalPrice=hotel.totalPrice,
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
    def get_hotel_by_request(cls, location, checkInDate, checkOutDate, guests, rooms, db_session):
        return db_session.query(cls).filter_by(location=location, checkInDate=checkInDate, checkOutDate=checkOutDate, guests=guests, rooms=rooms)
    
    @classmethod
    def get_hotel_by_budget(cls, location, checkInDate, checkOutDate, guests, rooms, budget, db_session):
        return db_session.query(cls).filter_by(location=location, checkInDate=checkInDate, checkOutDate=checkOutDate, guests=guests, rooms=rooms).filter(cls.totalPrice <= budget)

    @classmethod
    def update_hotel(cls, hotel_id, hotel: schema.HotelUpdate, db_session):
        """Update an existing flight."""
        hotel_obj = db_session.query(cls).filter_by(hotel_id=hotel_id).first()
        if hotel_obj:
            hotel_obj.name = hotel.name
            hotel_obj.location = hotel.location
            hotel_obj.checkInDate = hotel.checkInDate
            hotel_obj.checkOutDate = hotel.checkOutDate
            hotel_obj.guests = hotel.guests
            hotel_obj.rooms = hotel.rooms
            hotel_obj.reviewScore = hotel.reviewScore
            hotel_obj.totalPrice = hotel.totalPrice
            return hotel_obj
        else:
            return None
        
    # @classmethod
    # def suggestions(cls, location, checkInDate, checkOutDate, guests, rooms, price, db_session):
    #     cinDate = dt.strptime(checkInDate, '%Y-%m-%d')
    #     coutDate = dt.strptime(checkOutDate, '%Y-%m-%d')
    #     cinCls = dt.strptime(cls.checkInDate, '%Y-%m-%d')
    #     coutCls = dt.strptime(cls.checkOutDate, '%Y-%m-%d')
    #     return db_session.query(cls)\
    #         .filter_by(location=location, guests=guests, rooms=rooms)\
    #         .filter(cls.totalPrice <= price + 10 and cls.totalPrice >= price - 10)\
    #         .filter(cinCls >= cinDate - datetime.timedelta(2) and cinDate < coutDate)\
    #         .filter(coutCls <= coutDate + datetime.timedelta(days=2) and coutDate > cinDate)
    
class HotelBooking(Base):
    __tablename__ = 'hotel_booking'

    hotel_id = Column(Integer, ForeignKey('hotel.id'), primary_key=True)
    itinerary_id = Column(Integer, ForeignKey('itinerary.id'), primary_key=True)

    def __repr__(self):
        return f'<HotelBooking {self.hotel_id} {self.itinerary_id_id}>'

    @classmethod
    def create_hotel_booking(cls, hotel_booking: schema.HotelBookingCreate, db_session):
        """Create a new hotel booking."""
        hotel_booking_obj = cls(
            hotel_id=hotel_booking.hotel_id,
            itinerary_id=hotel_booking.itinerary_id
        )
        db_session.add(hotel_booking_obj)
        db_session.commit()
        return hotel_booking_obj

    @classmethod
    def get_hotel_booking(cls, hotel_id, itinerary_id, db_session):
        """Get a hotel booking by hotel_id and itinerary_id."""
        return db_session.query(cls).filter_by(hotel_id=hotel_id, itinerary_id_id=itinerary_id).first()

    @classmethod
    def get_all_hotel_bookings(cls, db_session):
        """Get all hotel bookings."""
        return db_session.query(cls).all()

    @classmethod
    def get_hotel_booking_by_itinerary_id(cls, itinerary_id, db_session):
        """Get all hotel bookings by itinerary_id."""
        return db_session.query(cls).filter_by(itinerary_id=itinerary_id).all()

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


    