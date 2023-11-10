from sqlalchemy import Column, Sequence, String, Integer
from database import Base
import passlib.hash
import schema

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email_address = Column(String, unique=True, primary_key=True, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    def verify_password(self, password):
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

    # @classmethod
    # def by_user_name(cls, username):
    #     """Return the user object whose user name is ``username``."""
    #     return SessionLocal.query(cls).filter_by(user_name=username).first()




