from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, security, status
from jose import ExpiredSignatureError, JWTError
from sqlalchemy import Column, Sequence, String, Integer
from sqlalchemy.orm import Session
from config import settings
from database import Base, get_db
from typing import Annotated, Union
import passlib.hash
import schema
import jwt
from .ItineraryModel import user_itinerary
from sqlalchemy.orm import relationship


oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="/token")

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, autoincrement=True, unique=True)
    email_address = Column(String, unique=True,
                           primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    itineraries = relationship("Itinerary", secondary=user_itinerary, back_populates="members")
    created_itineraries = relationship('Itinerary', back_populates='creator')

    def verify_password(self, password):
        """Verify that the provided password matches the user's password."""
        return passlib.hash.bcrypt.verify(password, self.hashed_password)

    def __repr__(self):
        return '<User: username=%s, email=%s>' % (
            repr(self.username),
            repr(self.email_address),
        )

    @classmethod
    def create_user(cls, user: schema.UserCreate, db_session):
        """Create a new user."""
        user_obj = cls(
            username=user.username,
            email_address=user.email_address,
            firstName=user.firstName,
            lastName=user.lastName,
            hashed_password=passlib.hash.bcrypt.hash(user.hashed_password)
        )
        db_session.add(user_obj)
        db_session.commit()
        return user_obj

    @classmethod
    def get_user_by_id(cls, user_id, db_session):
        """Return the user object whose id is ``user_id``."""
        return db_session.query(cls).filter_by(id=user_id).first()

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
            expire = datetime.utcnow() + timedelta(minutes=120)
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
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = schema.TokenData(email=email)
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except JWTError:
            raise credentials_exception
        
        user = cls.get_user_by_email(token_data.email, db)
        if user is None:
            raise credentials_exception
        
        userSchema = schema.UserModel(
            id=user.id, 
            email_address=user.email_address, 
            username=user.username, 
            firstName=user.firstName, 
            lastName=user.lastName)
        
        return userSchema
        # return schema.UserModel.model_validate(user)