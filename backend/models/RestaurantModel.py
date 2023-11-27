from sqlalchemy import Column, Sequence, ForeignKey, String, Integer, Float
from database import Base
import schema

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, Sequence('restaurant_id_seq'), primary_key=True)
    locationId = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    averageRating = Column(Float, nullable=False)
    userReviewCount = Column(Integer, nullable=False)
    priceTag = Column(String, nullable=False)
    menuURL = Column(String)

    @classmethod
    def create_restaurant(cls, restaurant: schema.RestaurantCreate, db_session):
        """Create a new restaurant."""
        restaurant_obj = cls(
            locationId = restaurant.locationId,
            name = restaurant.name,
            averageRating = restaurant.averageRating,
            userReviewCount = restaurant.userReviewCount,
            priceTag = restaurant.priceTag,
            menuURL = restaurant.menuURL
        )
        db_session.add(restaurant_obj)
        db_session.commit()
        return restaurant_obj
    
    
    
    @classmethod
    def checkLocationID(cls, locID, db_session):
        return db_session.query(cls).filter_by(locationId = locID).first()
    

class RestaurantBooking(Base):
    __tablename__ = 'restaurant_booking'

    geoID = Column(Integer, ForeignKey('restaurant.locationId'),primary_key = True)
    restaurantName = Column(String, ForeignKey('restaurant.name'),primary_key = True)
    itinerary_id = Column(Integer, ForeignKey('itinerary.id'), primary_key=True)

    def __repr__(self):
        return f'<RestaurantBooking {self.geoID} {self.restaurantName} {self.itinerary_id_id}>'

    @classmethod
    def create_restaurant_booking(cls, restaurant_booking: schema.RestaurantBookingCreate, db_session):
        """Create a new restaurant booking."""
        restaurant_booking_obj = cls(
            geoID = restaurant_booking.geoID,
            restaurantName = restaurant_booking.restaurantName,
            itinerary_id=restaurant_booking.itinerary_id
        )
        db_session.add(restaurant_booking_obj)
        db_session.commit()
        return restaurant_booking_obj

    @classmethod
    def get_restaurant_booking(cls, geoID, restaurantName, itinerary_id, db_session):
        return db_session.query(cls).filter_by(geoID=geoID, restaurantName = restaurantName, itinerary_id_id=itinerary_id).first()

    @classmethod
    def get_all_restaurant_bookings(cls, db_session):
        """Get all restaurant bookings."""
        return db_session.query(cls).all()

    @classmethod
    def get_restaurant_booking_by_itinerary_id(cls, itinerary_id, db_session):
        """Get all restaurant bookings by itinerary_id."""
        return db_session.query(cls).filter_by(itinerary_id=itinerary_id).all()

    @classmethod
    def delete_restaurant_booking(cls, geoID, restaurantName, itinerary_id, db_session):
        """Delete an existing restaurant booking."""
        restaurant_booking_obj = db_session.query(cls).filter_by(
            geoID = geoID, restaurantName = restaurantName, itinerary_id=itinerary_id).first()
        if restaurant_booking_obj:
            db_session.delete(restaurant_booking_obj)
            db_session.commit()
            return restaurant_booking_obj
        else:
            return None
    