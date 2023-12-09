from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr
from datetime import date

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
    checkInDate: date
    checkOutDate: date
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
    type: str

class LocationCreate(LocationBase):
    class Config:
        orm_mode = True

class LocationModel(LocationBase):
    class Config:
        orm_mode = True

# Itinerary Schema

class ItineraryBase(BaseModel):
    itineraryTitle: str
    destination: str
    departureAirport: str
    arrivalAirport: str
    departureDate: date
    returnDate: date
    # travelReason: str
    # leisureActivites: str
    budget: float
    creator_id: int
    rating: Optional[int] = None

class ItineraryCreate(ItineraryBase):
    members: Optional[List[EmailStr]] = []
    
    class Config:
        orm_mode = True

class ItineraryModel(ItineraryBase):
    id: int
    members: Optional[List[UserModel]] = []

    class Config:
        orm_mode = True

class ViewItinerary(ItineraryModel):
    creatorUsername: Optional[str] = None

class ItineraryUpdate(ItineraryModel):
    itineraryTitle: Optional[str]
    destination: Optional[str]
    departure: Optional[str]
    departureDate: Optional[date]
    returnDate: Optional[date]
    travelReason: Optional[str]
    leisureActivites: Optional[str]
    budget: Optional[float]
    creator_id: Optional[int]
    member_ids: Optional[List[int]]
    class Config:
        orm_mode = True


# Restaurant Schema

class RestaurantBase(BaseModel):
    locationId: int
    name: str
    averageRating: float
    userReviewCount: int
    priceTag: Optional[str]
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

class HotelBookingCreate(HotelBookingBase):
    class Config:
        orm_mode = True

class HotelBookingModel(HotelBookingBase):
    class Config:
        orm_mode = True

class HotelBookingUpdate(HotelBookingModel):
    class Config:
        orm_mode = True

class RestaurantBookingBase(BaseModel):
    geoID: int
    restaurantName: str
    itinerary_id: int
    restaurant_id: int

class RestaurantBookingCreate(RestaurantBookingBase):
    class Config:
        orm_mode = True

class RestaurantBookingModel(RestaurantBookingBase):
    class Config:
        orm_mode = True

class RestaurantBookingUpdate(RestaurantBookingBase):
    class Config:
        orm_mode = True



# Personal Finance Schema

class FinanceBase(BaseModel):
    email_address: str
    yearly_income: float
    monthly_spending: float
    estimated_savings: float
    travel_budget: float

class FinanceCreate(FinanceBase):
    class Config:
        orm_mode = True

class FinanceModel(FinanceBase):
    class Config:
        orm_mode = True

class FinanceUpdate(FinanceModel):
    class Config:
        orm_mode = True


# Savings Schema

class SavingsBase(BaseModel):
    email_address: str
    travel_budget: float
    goal: float
    period: str
    goal_per_period: Optional[float]
    progress_per_period: Optional[float]
    start_date: Optional[str]
    travel_date: Optional[str]

class SavingsCreate(SavingsBase):
    class Config:
        orm_mode = True

class SavingsModel(SavingsBase):
    class Config:
        orm_mode = True

class SavingsUpdate(SavingsModel):
    class Config:
        orm_mode = True

# Transaction Schema

class TransactionBase(BaseModel):
    email_address: str
    transaction_date: str
    transaction_amount: float

class TransactionCreate(TransactionBase):
    class Config:
        orm_mode = True

class TransactionModel(TransactionBase):
    transaction_id: int
    class Config:
        orm_mode = True
        






