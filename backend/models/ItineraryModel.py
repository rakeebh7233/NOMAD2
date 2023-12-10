from sqlalchemy import CheckConstraint, Column, Sequence, ForeignKey, String, Integer, Table, Date, Float
from database import Base
import schema
from sqlalchemy.orm import relationship
from . import UserModel, FlightModel, HotelModel
import datetime

# Association table
user_itinerary = Table('user_itinerary', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('itinerary_id', Integer, ForeignKey('itinerary.id'))
)

class Itinerary(Base):
    __tablename__ = 'itinerary'

    id = Column(Integer, Sequence('itinerary_id_seq'), primary_key=True, autoincrement=True)
    itineraryTitle = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departureAirport = Column(String, nullable=False)
    arrivalAirport = Column(String, nullable=False)
    departureDate = Column(Date, nullable=False)
    returnDate = Column(Date, nullable=False)
    budget = Column(Float, nullable=False)
    creator_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    rating = Column(Integer, nullable=True)  
    
    # Add a check constraint for the rating
    __table_args__ = (CheckConstraint('rating >= 1 AND rating <= 5', name='rating_check'), )
    
    # Relationship to User
    members = relationship('User', secondary=user_itinerary, back_populates='itineraries')
    creator = relationship('User', back_populates='created_itineraries')

    def __repr__(self):
        return f'<Itinerary {self.id}>'

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
        
    @classmethod
    def get_user_itinerary_id(cls, user_id, db_session):
        """Get the first itinerary_id from the user_itinerary table based on a passed user_id parameter."""
        query = db_session.query(user_itinerary).filter_by(user_id=user_id).first()
        if query:
            return query.itinerary_id
        else:
            return None
        
    # this function is called in "update_progress" of Finance Model, to update the travel date of user
    @classmethod
    def get_earliest_departure_date(cls, email_address, db_session):
        user_id = db_session.query(UserModel.User).filter_by(email_address=email_address).first().id
        print(user_id)
        itineraries = db_session.query(user_itinerary).filter(user_id == user_id).all()
        print(itineraries)
        current_date = datetime.datetime.now().date()
        earliest_departure_date = None
        for itinerary in itineraries:
            departure_date = db_session.query(cls).filter(cls.id == itinerary.itinerary_id).first().departureDate
            if departure_date <= current_date:
                continue
            if earliest_departure_date == None:
                earliest_departure_date = departure_date
            elif departure_date < earliest_departure_date:
                earliest_departure_date = departure_date
        if earliest_departure_date == None:
            return -1
        return earliest_departure_date
    
    @classmethod
    def get_itinerary_by_email_and_departure_date(cls, email_address, departure_date, db_session):
        user_id = db_session.query(UserModel.User).filter_by(email_address=email_address).first().id
        print(user_id)
        itineraries = db_session.query(user_itinerary).filter(user_id == user_id).all()
        print(itineraries)
        for itinerary in itineraries:
            itinerary_obj = db_session.query(cls).filter(cls.id == itinerary.itinerary_id).first()
            if itinerary_obj.departureDate == departure_date:
                return itinerary_obj.id
        return None
    
    # this function is called in "update_progress" of Finance Model, to update the savings goal of user
    @classmethod
    def get_itinerary_price(cls, itinerary_id, db_session):
        if itinerary_id == None:
            return 0
        itinerary = db_session.query(cls).filter_by(id=itinerary_id).first()
        if not itinerary:
            return 0
        price = 0


        flight_bookings = db_session.query(FlightModel.FlightBooking).filter_by(itinerary_id=itinerary.id).all()
        print(flight_bookings)
        for flight_booking in flight_bookings:
            flight = db_session.query(FlightModel.Flight).filter_by(id=flight_booking.flight_id).first()
            price += flight.totalPrice

        hotel_bookings = db_session.query(HotelModel.HotelBooking).filter_by(itinerary_id=itinerary.id).all()
        print(hotel_bookings)
        for hotel_booking in hotel_bookings:
            hotel = db_session.query(HotelModel.Hotel).filter_by(id=hotel_booking.hotel_id).first()
            price += hotel.totalPrice

        return price
    

    

            