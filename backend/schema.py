from typing import Optional, Union
from pydantic import BaseModel

# This file uses pydantic to validate the incoming data from the frontend

# User Schema
class UserBase(BaseModel):
    username: str
    email_address: str
    firstName: str
    lastName: str

class UserCreate(UserBase):
    hashed_password: str
    class Config:
        orm_mode = True

class UserModel(UserBase):
    id: int
    class Config:
        orm_mode = True

# Token Schema

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None

# Flight Schema

class FlightBase(BaseModel):
    departureAirport: str
    arrivalAirport: str
    departureTime: str #switch to date 
    arrivalTime: str #switch to date
    cabinClass: str
    carrier: str
    totalPrice: float

class FlightCreate(FlightBase):
    class Config:
        orm_mode = True

class FlightModel(FlightBase):
    id: int
    class Config:
        orm_mode = True
    
class FlightUpdate(FlightBase):
    class Config:
        orm_mode = True

# Hotel Schema

class HotelBase(BaseModel):
    name: str
    location: str
    checkInDate: str
    checkOutDate: str
    guests: int
    rooms: int
    reviewScore: float
    totalPrice: float

class HotelCreate(HotelBase):
    class Config:
        orm_mode = True

class HotelModel(HotelBase):
    id: int
    class Config:
        orm_mode = True

class HotelUpdate(HotelModel):
    class Config:
        orm_mode = True

# Location Schema

class LocationBase(BaseModel):
    name: str
    geoId: int

class LocationCreate(LocationBase):
    class Config:
        orm_mode = True

class LocationModel(LocationBase):
    class Config:
        orm_mode = True

# Itinerary Schema

class ItineraryBase(BaseModel):
    flight_id: int
    hotel_id: int
    destination: str

class ItineraryCreate(ItineraryBase):
    class Config:
        orm_mode = True

class ItineraryModel(ItineraryBase):
    id: int
    class Config:
        orm_mode = True

class ItineraryUpdate(ItineraryModel):
    class Config:
        orm_mode = True

# Itinerary Owner Schema

class ItineraryOwnerBase(BaseModel):
    itinerary_id: int
    user_id: int

class ItineraryOwnerCreate(ItineraryOwnerBase):
    class Config:
        orm_mode = True

class ItineraryOwnerModel(ItineraryOwnerBase):
    class Config:
        orm_mode = True

class ItineraryOwnerUpdate(ItineraryOwnerModel):
    class Config:
        orm_mode = True

# Restaurant Schema

class RestaurantBase(BaseModel):
    locationId: int
    name: str
    averageRating: float
    userReviewCount: int
    priceTag: str
    menuURL: Union[str, None] = None

class RestaurantCreate(RestaurantBase):
    class Config:
        orm_mode = True

class RestaurantModel(RestaurantBase):
    id: int
    class Config:
        orm_mode = True

class RestaurantUpdate(RestaurantBase):
    class Config:
        orm_mode = True

# Booking Schemas

class FlightBookingBase(BaseModel):
    flight_id: int
    itinerary_id: int
    cabinClass: str
    totalPrice: float

class FlightBookingCreate(FlightBookingBase):
    class Config:
        orm_mode = True

class FlightBookingModel(FlightBookingBase):
    class Config:
        orm_mode = True

class FlightBookingUpdate(FlightBookingModel):
    class Config:
        orm_mode = True

class HotelBookingBase(BaseModel):
    hotel_id: int
    itinerary_id: int
    totalPrice: float

class HotelBookingCreate(HotelBookingBase):
    class Config:
        orm_mode = True

class HotelBookingModel(HotelBookingBase):
    class Config:
        orm_mode = True

class HotelBookingUpdate(HotelBookingModel):
    class Config:
        orm_mode = True







