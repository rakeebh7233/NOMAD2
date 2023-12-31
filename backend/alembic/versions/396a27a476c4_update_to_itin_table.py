"""update to Itin Table

Revision ID: 396a27a476c4
Revises: 
Create Date: 2023-11-25 14:48:47.095115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '396a27a476c4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('DROP TABLE IF EXISTS "user" CASCADE')
    op.drop_table('savings')
    op.drop_table('location')
    op.drop_table('flight_booking')
    op.execute('DROP TABLE IF EXISTS "hotel" CASCADE')
    op.drop_table('hotel_booking')
    op.drop_table('flight')
    op.drop_table('user_itinerary')
    op.drop_table('restaurant')
    op.drop_table('personal_finance')
    op.execute('DROP TABLE IF EXISTS "itinerary" CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('itinerary',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('itineraryName', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('destination', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('departure', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('departureDate', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('returnDate', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('travelReason', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('leisureActivites', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('budget', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('creator_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], name='itinerary_creator_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='itinerary_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('personal_finance',
    sa.Column('email_address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('yearly_income', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('monthly_spending', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('estimated_savings', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('travel_budget', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['email_address'], ['user.email_address'], name='personal_finance_email_address_fkey'),
    sa.PrimaryKeyConstraint('email_address', name='personal_finance_pkey')
    )
    op.create_table('restaurant',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('locationId', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('averageRating', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('userReviewCount', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('priceTag', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('menuURL', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='restaurant_pkey')
    )
    op.create_table('user_itinerary',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('itinerary_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['itinerary_id'], ['itinerary.id'], name='user_itinerary_itinerary_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_itinerary_user_id_fkey')
    )
    op.create_table('flight',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('departureAirport', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('arrivalAirport', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('departureTime', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('arrivalTime', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('cabinClass', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('carrier', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('totalPrice', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='flight_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('hotel_booking',
    sa.Column('hotel_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('itinerary_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotel.id'], name='hotel_booking_hotel_id_fkey'),
    sa.ForeignKeyConstraint(['itinerary_id'], ['itinerary.id'], name='hotel_booking_itinerary_id_fkey'),
    sa.PrimaryKeyConstraint('hotel_id', 'itinerary_id', name='hotel_booking_pkey')
    )
    op.create_table('hotel',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('location', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('checkInDate', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('checkOutDate', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('guests', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rooms', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('reviewScore', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('totalPrice', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='hotel_pkey')
    )
    op.create_table('flight_booking',
    sa.Column('flight_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('itinerary_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['flight_id'], ['flight.id'], name='flight_booking_flight_id_fkey'),
    sa.ForeignKeyConstraint(['itinerary_id'], ['itinerary.id'], name='flight_booking_itinerary_id_fkey'),
    sa.PrimaryKeyConstraint('flight_id', 'itinerary_id', name='flight_booking_pkey')
    )
    op.create_table('location',
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('geoId', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('name', name='location_pkey')
    )
    op.create_table('savings',
    sa.Column('email_address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('current_budget', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('goal', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('period', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('goal_per_period', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('progress_per_period', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('start_date', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('travel_date', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['email_address'], ['user.email_address'], name='savings_email_address_fkey'),
    sa.PrimaryKeyConstraint('email_address', name='savings_pkey')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('email_address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('firstName', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('lastName', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', 'email_address', name='user_pkey'),
    sa.UniqueConstraint('email_address', name='user_email_address_key'),
    sa.UniqueConstraint('id', name='user_id_key'),
    sa.UniqueConstraint('username', name='user_username_key')
    )
    # ### end Alembic commands ###
