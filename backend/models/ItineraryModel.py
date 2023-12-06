from sqlalchemy import CheckConstraint, Column, Sequence, ForeignKey, String, Integer, Table, Date, Float
from database import Base
import schema
from sqlalchemy.orm import relationship

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
    departure = Column(String, nullable=False)
    departureDate = Column(Date, nullable=False)
    returnDate = Column(Date, nullable=False)
    travelReason = Column(String, nullable=False)
    leisureActivites = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    creator_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    rating = Column(Integer, nullable=True)  # Change this line
    
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