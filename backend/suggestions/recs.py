import pandas as pd
import numpy as np
import psycopg2

from sklearn.metrics.pairwise import cosine_similarity

def execute_query(query):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database="nomad",
        user="postgres",
        password="1234"
    )
    # Create a cursor object to execute the query
    cur = conn.cursor()
    try:
        # Execute the query
        cur.execute(query)
        # Retrieve query results and put into pandas dataframe
        col_names = []
        for elt in cur.description:
            col_names.append(elt[0])
        results = pd.DataFrame(cur.fetchall(), columns=col_names)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error executing query:", error)

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
        return results
    
def load_flight_data():
    flights = execute_query("SELECT * FROM flight")
    return flights

def load_hotel_data():
    hotels = execute_query("SELECT * FROM hotel")
    return hotels

def create_picot_table_flights(flights):
    # Create a pivot table
    pivot_table = flights.pivot_table(index='id', columns=['departureAirport','arrivalAirport','cabinClass'], values='totalPrice').fillna(0)
    return pivot_table

def create_picot_table_hotels(hotels):
    # Create a pivot table
    pivot_table = hotels.pivot_table(index='id', columns=['name','location','checkInDate', 'checkOutDate', 'guests', 'rooms'], values='reviewScore').fillna(0)
    return pivot_table

def findSimilarFlights(flight_id, pivot_table):
    # Find similar flights
    flight = pivot_table.loc[flight_id].values.reshape(1,-1)
    similarity = []
    for i,row in enumerate(pivot_table.values):
        cos = cosine_similarity(flight, row.reshape(1,-1))[0][0]
        similarity.append([i, cos])
    temp = pd.DataFrame(similarity, columns=['id', 'similarity'])
    temp = temp.sort_values(by='similarity', ascending=False)
    similar_flights = list(temp['id'].values)
    return similar_flights

def findSimilarHotels(hotel_id, pivot_table):
    # Find similar hotels
    hotel = pivot_table.loc[hotel_id].values.reshape(1,-1)
    similarity = []
    for i,row in enumerate(pivot_table.values):
        cos = cosine_similarity(hotel, row.reshape(1,-1))[0][0]
        similarity.append([i, cos])
    temp = pd.DataFrame(similarity, columns=['id', 'similarity'])
    temp = temp.sort_values(by='similarity', ascending=False)
    similar_hotels = list(temp['id'].values)
    return similar_hotels

def get_flight_suggestions(flight_id):
    flights = load_flight_data()
    pivot_table = create_picot_table_flights(flights)
    similar_flights = findSimilarFlights(flight_id, pivot_table)
    return similar_flights[0:5]

def get_hotel_suggestions(hotel_id):
    hotels = load_hotel_data()
    pivot_table = create_picot_table_hotels(hotels)
    similar_hotels = findSimilarHotels(hotel_id, pivot_table)
    return similar_hotels[0:5]
