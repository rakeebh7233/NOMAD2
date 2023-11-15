from sqlalchemy import Column, Sequence, ForeignKey, String, Integer, Float
from database import Base
import schema

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