from sqlalchemy import VARCHAR, Column, String
from database import Base

class User(Base):
    __tablename__ = 'user'

    email_address = Column(String(100), unique=True, primary_key=True, nullable=False)
    firstName = Column(String(100), nullable=False)
    lastName = Column(VARCHAR(100), nullable=False)
    hashed_password = Column(VARCHAR(100))

    def __repr__(self):
        return '<User: name=%s, email=%s>' % (
            repr(self.firstName + ' ' + self.lastName),
            repr(self.email_address),
        )

    # def __unicode__(self):
    #     return self.firstName + ' ' + self.lastName

    # @classmethod
    # def by_email_address(cls, email):
    #     """Return the user object whose email address is ``email``."""
    #     return SessionLocal.query(cls).filter_by(email_address=email).first()

    # @classmethod
    # def by_user_name(cls, username):
    #     """Return the user object whose user name is ``username``."""
    #     return SessionLocal.query(cls).filter_by(user_name=username).first()

    # @classmethod
    # def _hash_password(cls, password):
    #     salt = sha256()
    #     salt.update(os.urandom(60))
    #     salt = salt.hexdigest()

    #     hash = sha256()
    #     # Make sure password is a str because we cannot hash unicode objects
    #     hash.update((password + salt).encode('utf-8'))
    #     hash = hash.hexdigest()

    #     password = salt + hash


    #     return password

    # def _set_password(self, password):
    #     """Hash ``password`` on the fly and store its hashed version."""
    #     self._password = self._hash_password(password)

    # def _get_password(self):
    #     """Return the hashed version of the password."""
    #     return self._password

    # password = synonym('_password', descriptor=property(_get_password,
    #                                                     _set_password))

    # def validate_password(self, password):
    #     """
    #     Check the password against existing credentials.

    #     :param password: the password that was provided by the user to
    #         try and authenticate. This is the clear text version that we will
    #         need to match against the hashed one in the database.
    #     :type password: unicode object.
    #     :return: Whether the password is valid.
    #     :rtype: bool

    #     """
    #     hash = sha256()
    #     hash.update((password + self.password[:64]).encode('utf-8'))
    #     return self.password[64:] == hash.hexdigest()



