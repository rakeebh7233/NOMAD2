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
    