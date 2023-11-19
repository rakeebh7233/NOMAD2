from sqlalchemy import Column, Sequence, ForeignKey, String, Integer, Float
from database import Base
from datetime import datetime, date, timedelta
import schema
from .UserModel import User


# The Personal Finance table will store the preliminary financial information that the user provides
# We will use these features to generate finance based recommendations
class PersonalFinance(Base):
    __tablename__ = 'personal_finance'

    email_address = Column(String, ForeignKey('user.email_address'), primary_key=True)
    yearly_income = Column(Float, nullable=False)
    monthly_spending = Column(Float, nullable=False)
    estimated_savings = Column(Float, nullable=False)
    travel_budget = Column(Float, nullable=False)

    def __repr__(self):
        return '<Personal Finance: email_address=%s, yearly_income=%s, monthly_spending=%s, estimated_savings=%s, travel_budget=%s>' % (
            repr(self.email_address),
            repr(self.yearly_income),
            repr(self.monthly_spending),
            repr(self.estimated_savings),
            repr(self.travel_budget)
        )
    
    @classmethod
    def create_finance(cls, db_session, request: schema.FinanceCreate):
        """Create a new personal finance."""
        finance_obj = cls(
            email_address=request.email_address,
            yearly_income=request.yearly_income,
            monthly_spending=request.monthly_spending,
            estimated_savings=request.estimated_savings,
            travel_budget=request.travel_budget
        )
        db_session.add(finance_obj)
        db_session.commit()
        return finance_obj
    
    @classmethod
    def update_finance(cls, db_session, email_address, request: schema.FinanceCreate):
        """Update an existing personal finance."""
        finance_obj = cls.get_finance_user(db_session, email_address)
        if finance_obj == None:
            return None
        finance_obj.yearly_income = request.yearly_income
        finance_obj.monthly_spending = request.monthly_spending
        finance_obj.estimated_savings = request.estimated_savings
        finance_obj.travel_budget = request.travel_budget
        db_session.commit()
        return finance_obj
    
    @classmethod
    def get_finance_user(cls, db_session, email_address):
        """Return the personal finance object whose user_id is ``id``."""
        return db_session.query(cls).filter_by(email_address=email_address).first()
    
    @classmethod
    def delete_finance(cls, db_session, email_address):
        """Delete the personal finance object whose user_id is ``id``."""
        finance_obj = cls.get_finance_user(db_session, email_address)
        if finance_obj == None:
            return None
        db_session.delete(finance_obj)
        db_session.commit()
        return finance_obj
    

    
# The Savings tables will store the budget goals and updates for the user to progress towards
# This can be used for reccommendation and finance based itineraries 
class Savings(Base):
    __tablename__ = 'savings'

    email_address = Column(String, ForeignKey('user.email_address'), primary_key=True)
    current_budget = Column(Float, nullable=False)
    goal = Column(Float, nullable=False)

    period = Column(String, nullable=False)
    goal_per_period = Column(Float, nullable=False)
    progress_per_period = Column(Float, nullable=False)
    start_date = Column(String, nullable=False)
    travel_date = Column(String, nullable=False)

    def __repr__(self):
        return '<Savings: email_address=%s, current_budget=%s, goal=%s, period=%s, goal_per_period=%s, progress_per_period=%s>' % (
            repr(self.email_address),
            repr(self.current_budget),
            repr(self.goal),
            repr(self.period),
            repr(self.goal_per_period),
            repr(self.progress_per_period),
            repr(self.start_date),
            repr(self.travel_date)
        )
    
    @classmethod
    def create_savings(cls, db_session, request: schema.SavingsCreate):
        """Create a new savings goal."""
        savings_obj = cls(
            email_address=request.email_address,
            current_budget=request.current_budget,
            goal=request.goal,
            period=request.period,
            goal_per_period=cls.update_goal_per_period(request.goal, request.current_budget, request.period, request.travel_date),
            progress_per_period=0.0,
            start_date=date.today(),
            travel_date=request.travel_date
        )
        db_session.add(savings_obj)
        db_session.commit()
        return savings_obj
    
    @classmethod
    def update_savings(cls, db_session, email_address, request: schema.SavingsCreate):
        """Update an existing savings goal."""
        savings_obj = cls.get_savings_user(db_session, email_address)
        if savings_obj == None:
            return None
        savings_obj.current_budget = request.current_budget
        savings_obj.goal = request.goal
        savings_obj.period = request.period
        # goal per period will be updated with progress per period
        savings_obj.progress_per_period = cls.update_progress(request.current_budget, request.period, request.travel_date)
        savings_obj.start_date = request.start_date
        savings_obj.travel_date = request.travel_date
        db_session.commit()
        return savings_obj
    
    @classmethod
    def get_savings_user(cls, db_session, email_address):
        """Return the savings object whose user_id is ``id``."""
        return db_session.query(cls).filter_by(email_address=email_address).first()
    
    @classmethod
    def update_goal_per_period(goal, current_budget, period, travel_date):

        today = date.today()
        d1 = datetime.strptime(today, "%Y/%m/%d")
        d2 = datetime.strptime(travel_date, "%Y/%m/%d")
        remaining_goal = goal - current_budget

        if (period.lower() == "weekly"):
            return remaining_goal / ((d2 - d1).days / 7)
        elif (period.lower() == "monthly"):
            return remaining_goal / ((d2 - d1).days / 30)
        elif (period.lower() == "yearly"):
            return remaining_goal / ((d2 - d1).days / 365)
        else:
            return None
        
    @classmethod
    def update_progress(cls, db_session, email_address, progress):
        savings_obj = cls.get_savings_user(db_session, email_address)
        if savings_obj is None:
            return None

        savings_obj.progress_per_period += progress
        savings_obj.current_budget += progress
        savings_obj.goal_per_period = cls.update_goal_per_period(savings_obj.goal, savings_obj.current_budget, savings_obj.period, savings_obj.travel_date)

        db_session.commit()
        return savings_obj
    
    @classmethod
    def reset_progress_per_period(cls, db_session, email_address): 
        """Reset the progress_per_period to 0 based on the goal and period."""

        savings_obj = cls.get_savings_user(db_session, email_address)

        today = date.today()
        d1 = datetime.strptime(today, "%Y/%m/%d")
        d2 = datetime.strptime(savings_obj.travel_date, "%Y/%m/%d")

        if savings_obj.period.lower() == "weekly":
            if (d2 - d1).days % 7 == 0:
                savings_obj.progress_per_period = 0
        elif savings_obj.period.lower() == "monthly":
            if (d2 - d1).days % 30 == 0:
                savings_obj.progress_per_period = 0
        elif savings_obj.period.lower() == "yearly":
            if (d2 - d1).days % 365 == 0:
                savings_obj.progress_per_period = 0
        else:
            return None

        db_session.commit()
        
    @classmethod
    def check_period_success(cls, db_session, email_address):
        """Check if the user has successfully saved enough money for the period."""
        savings_obj = db_session.query(cls).filter_by(email_address=email_address).first()
        if savings_obj.progress_per_period >= savings_obj.goal_per_period:
            return True
        return False
    
    @classmethod
    def check_savings_success(cls, db_session, email_address):
        """Check if the user has successfully saved enough money for the trip."""
        savings_obj = db_session.query(cls).filter_by(email_address=email_address).first()
        if savings_obj.current_budget >= savings_obj.goal:
            return True
        return False
    
    @classmethod
    def delete_savings(cls, db_session, email_address):
        """Delete the savings object whose user_id is ``id``."""
        savings_obj = cls.get_savings_user(db_session, email_address)
        if savings_obj == None:
            return None
        db_session.delete(savings_obj)
        db_session.commit()
        return savings_obj
     


