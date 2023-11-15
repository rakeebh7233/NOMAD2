from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, security, status
from jose import JWTError
from sqlalchemy import Column, Sequence, ForeignKey, String, Integer, Float, Date
from sqlalchemy.orm import Session
from config import settings
from database import Base, db_dependency, get_db
from typing import Annotated, Union
import passlib.hash
import schema
import jwt

oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="/token")

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email_address = Column(String, unique=True,
                           primary_key=True, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    def verify_password(self, password):
        """Verify that the provided password matches the user's password."""
        return passlib.hash.bcrypt.verify(password, self.hashed_password)

    def __repr__(self):
        return '<User: name=%s, email=%s>' % (
            repr(self.firstName + ' ' + self.lastName),
            repr(self.email_address),
        )

    @classmethod
    def create_user(cls, user: schema.UserCreate, db_session):
        """Create a new user."""
        user_obj = cls(
            email_address=user.email_address,
            firstName=user.firstName,
            lastName=user.lastName,
            hashed_password=passlib.hash.bcrypt.hash(user.hashed_password)
        )
        db_session.add(user_obj)
        db_session.commit()
        return user_obj

    @classmethod
    def get_user_by_email(cls, email, db_session):
        """Return the user object whose email address is ``email``."""
        return db_session.query(cls).filter_by(email_address=email).first()

    @classmethod
    def authenticate_user(cls, email, password, db_session):
        """Verify that the user exists and that the password is correct."""
        user = cls.get_user_by_email(email, db_session)
        if not user:
            return False
        if not user.verify_password(password):
            return False
        return user

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    @classmethod
    def get_current_user(cls, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = schema.TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = cls.get_user_by_email(token_data.username, db)
        if user is None:
            raise credentials_exception
        user2 = schema.UserModel(id=user.id, email_address=user.email_address, firstName=user.firstName, lastName=user.lastName)
        return user2
        # return schema.UserModel.model_validate(user)


class Flight(Base):
    __tablename__ = 'flight'

    id = Column(Integer, Sequence('flight_id_seq'), primary_key=True)
    departureAirport = Column(String, nullable=False)
    arrivalAirport = Column(String, nullable=False)
    departureTime = Column(String, nullable=False)
    arrivalTime = Column(String, nullable=False)
    cabinClass = Column(String, nullable=False)
    carrier = Column(String, nullable=False)

    def __repr__(self):
        return '<Flight: departureAirport=%s, arrivalAirport=%s, departureTime=%s, arrivalTime=%s, cabinClass=%s, carrier=%s, currency=%s, total_price=%s>' % (
            repr(self.departureAirport),
            repr(self.arrivalAirport),
            repr(self.departureTime),
            repr(self.arrivalTime),
            repr(self.cabinClass),
            repr(self.carrier),
        )

    @classmethod
    def create_flight(cls, flight: schema.FlightCreate, db_session):
        """Create a new flight."""
        flight_obj = cls(
            departureAirport=flight.departureAirport,
            arrivalAirport=flight.arrivalAirport,
            departureTime=flight.departureTime,
            arrivalTime=flight.arrivalTime,
            cabinClass=flight.cabinClass,
            carrier=flight.carrier,
        )
        db_session.add(flight_obj)
        db_session.commit()
        return flight_obj

    @classmethod
    def get_all_flights(cls, db_session):
        return db_session.query(cls).all()

    @classmethod
    def get_flight_by_id(cls, flight_id, db_session):
        return db_session.query(cls).filter_by(id=flight_id).first()

    @classmethod
    def get_flight_by_request(cls, departureAirport, arrivalAirport, departureTime, arrivalTime, cabinClass, db_session):
        return db_session.query(cls).filter_by(
            departureAirport=departureAirport,
            arrivalAirport=arrivalAirport,
            departureTime=departureTime,
            arrivalTime=arrivalTime,
            cabinClass=cabinClass,
            )
    
    @classmethod
    def update_flight(cls, flight_id, flight: schema.FlightUpdate, db_session):
        """Update an existing flight."""
        flight_obj = db_session.query(cls).filter_by(id=flight_id).first()
        if flight_obj:
            flight_obj.departureAirport = flight.departureAirport
            flight_obj.arrivalAirport = flight.arrivalAirport
            flight_obj.departureTime = flight.departureTime
            flight_obj.arrivalTime = flight.arrivalTime
            flight_obj.cabinClass = flight.cabinClass
            flight_obj.carrier = flight.carrier
            db_session.commit()
            return flight_obj
        else:
            return None


class FlightBooking(Base):
    __tablename__ = 'flight_booking'

    flight_id = Column(Integer, ForeignKey('flight.id'), primary_key=True)
    itinerary_id = Column(Integer, ForeignKey(
        'itinerary.id'), primary_key=True)
    cabinClass = Column(String, nullable=False)
    totalPrice = Column(Float, nullable=False)

    def __repr__(self):
        return f'<FlightBooking {self.flight_id} {self.itinerary_id}>'

    @classmethod
    def create_flight_booking(cls, flight_booking: schema.FlightBookingCreate, db_session):
        """Create a new flight booking."""
        flight_booking_obj = cls(
            flight_id=flight_booking.flight_id,
            itinerary_id=flight_booking.itinerary_id,
            cabinClass=flight_booking.cabinClass,
            totalPrice=flight_booking.totalPrice,
        )
        db_session.add(flight_booking_obj)
        db_session.commit()
        return flight_booking_obj

    @classmethod
    def get_flight_booking(cls, flight_id, itinerary_id, db_session):
        """Get a flight booking by flight_id and user_id."""
        return db_session.query(cls).filter_by(flight_id=flight_id, itinerary_id=itinerary_id).first()

    @classmethod
    def get_all_flight_bookings(cls, db_session):
        """Get all flight bookings."""
        return db_session.query(cls).all()

    @classmethod
    def update_flight_booking(cls, flight_id, itinerary_id, flight_booking: schema.FlightBookingUpdate, db_session):
        """Update an existing flight booking."""
        flight_booking_obj = db_session.query(cls).filter_by(
            flight_id=flight_id, itinerary_id=itinerary_id).first()
        if flight_booking_obj:
            flight_booking_obj.cabinClass = flight_booking.cabinClass
            flight_booking_obj.totalPrice = flight_booking.totalPrice
            db_session.commit()
            return flight_booking_obj
        else:
            return None

    @classmethod
    def delete_flight_booking(cls, flight_id, itinerary_id, db_session):
        """Delete an existing flight booking."""
        flight_booking_obj = db_session.query(cls).filter_by(
            flight_id=flight_id, itinerary_id=itinerary_id).first()
        if flight_booking_obj:
            db_session.delete(flight_booking_obj)
            db_session.commit()
            return flight_booking_obj
        else:
            return None


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


class Itinerary(Base):
    __tablename__ = 'itinerary'

    id = Column(Integer, Sequence('itinerary_id_seq'), primary_key=True)
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
