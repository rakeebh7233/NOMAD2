import sys 
sys.path.append("..")
from models import FlightModel, HotelModel
from fastapi import Depends
import schema, database
from sqlalchemy.orm import Session
from typing import List

import psycopg2
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import DataLoader, Dataset, TensorDataset

get_db = database.get_db



def execute_query(query, table_name):
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

        # Fetch all the rows from the result
        rows = cur.fetchall()

        # Do something with the rows (e.g., print them)
        results = []
        if table_name == "flight":
            for row in rows:
                flight = schema.FlightModel(id=row[0], departureAirport=row[1], arrivalAirport=row[2], departureTime=row[3], 
                                            arrivalTime=row[4], cabinClass=row[5], carrier=row[6], totalPrice=row[7])
                results.append(flight)
        elif table_name == "hotel":
            for row in rows:
                hotel = schema.HotelModel(id=row[0], name=row[1], location=row[2], checkInDate=row[3], checkOutDate=row[4],
                                            guests=row[5], rooms=row[6], reviewScore=row[7], totalPrice=row[8])
                results.append(hotel)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error executing query:", error)

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
        return results





# Define the recommender system model
class RecommenderSystem(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RecommenderSystem, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        # print("FC1: ", type(self.fc1.weight.dtype))
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Load flight data from the Flight table
def load_flight_data() -> List[schema.FlightModel]:
    #flights = db.query(FlightModel.Flight).all()
    flights = execute_query("SELECT * FROM flight", "flight")
    return flights

# Load hotel data from the Hotel table
def load_hotel_data(db: Session = Depends(get_db)) -> List[schema.HotelModel]:
    hotels = db.query(HotelModel.Hotel).all()
    return hotels
    

# Prepare flight input data for training the recommender system
def prepare_flight_data(flights: List[schema.FlightModel]) -> (torch.Tensor, torch.Tensor):

    # Calculate the number of flights to include in the input data (80% training data)
    num_flights = len(flights)
    num_input_flights = int(0.8 * num_flights)

    # Select the first 80% of flights for the input (training) data
    input_flights = flights[:num_input_flights]
    input_flights = encode_flight_data(input_flights)
    # Select the remaining 20% of flights for the test data
    test_flights = flights[num_input_flights:]
    test_flights = encode_flight_data(test_flights)  

    # Convert flight information to input tensor with numeric mappings
    training_data = torch.tensor(input_flights, dtype=torch.float32)
    test_data = torch.tensor(test_flights, dtype=torch.float32)
    return training_data, test_data

def encode_flight_data(flights: List[schema.FlightModel]) -> List[schema.FlightModel]:
    # Create a LabelEncoder instance
    label_encoder = LabelEncoder()

    # Get the IDs from each flight
    flight_ids = [flight.id for flight in flights]
    # Encode the flight IDs
    encoded_ids = label_encoder.fit_transform(flight_ids)
    # Replace the IDs in each flight
    for i, flight in enumerate(flights):
        flight.id = encoded_ids[i]

    # Get the departure airports from each flight
    departure_airports = [flight.departureAirport for flight in flights]
    # Encode the departure airports
    encoded_departure_airports = label_encoder.fit_transform(departure_airports)
    # Replace the departure airports in each flight
    for i, flight in enumerate(flights):
        flight.departureAirport = encoded_departure_airports[i]

    # Get the arrival airports from each flight
    arrival_airports = [flight.arrivalAirport for flight in flights]
    # Encode the arrival airports
    encoded_arrival_airports = label_encoder.fit_transform(arrival_airports)
    # Replace the arrival airports in each flight
    for i, flight in enumerate(flights):
        flight.arrivalAirport = encoded_arrival_airports[i]

    # Get the departure times from each flight
    departure_times = [flight.departureTime for flight in flights]
    # Encode the departure times
    encoded_departure_times = label_encoder.fit_transform(departure_times)
    # Replace the departure times in each flight
    for i, flight in enumerate(flights):
        flight.departureTime = encoded_departure_times[i]

    # Get the arrival times from each flight
    arrival_times = [flight.arrivalTime for flight in flights]
    # Encode the arrival times
    encoded_arrival_times = label_encoder.fit_transform(arrival_times)
    # Replace the arrival times in each flight
    for i, flight in enumerate(flights):
        flight.arrivalTime = encoded_arrival_times[i]

    # Get the cabin classes from each flight
    cabin_classes = [flight.cabinClass for flight in flights]
    # Encode the cabin classes
    encoded_cabin_classes = label_encoder.fit_transform(cabin_classes)
    # Replace the cabin classes in each flight
    for i, flight in enumerate(flights):
        flight.cabinClass = encoded_cabin_classes[i]

    # Get the carriers from each flight
    carriers = [flight.carrier for flight in flights]
    # Encode the carriers
    encoded_carriers = label_encoder.fit_transform(carriers)
    # Replace the carriers in each flight
    for i, flight in enumerate(flights):
        flight.carrier = encoded_carriers[i]

    # Get the total prices from each flight
    total_prices = [flight.totalPrice for flight in flights]
    # Encode the total prices
    encoded_total_prices = label_encoder.fit_transform(total_prices)
    # Replace the total prices in each flight
    for i, flight in enumerate(flights):
        flight.totalPrice = encoded_total_prices[i]

    flights_list = []
    for flight in flights:
        new_flight = [flight.id, flight.departureAirport, flight.arrivalAirport, flight.departureTime, flight.arrivalTime, flight.cabinClass, flight.carrier, flight.totalPrice]
        #print(new_flight)
        flights_list.append(new_flight)

    #print(flights_list)
    return flights_list

    

# Prepare hotel input data for training the recommender system
def prepare_hotel_data(hotels: List[HotelModel.Hotel]) -> torch.Tensor:
    # Calculate the number of hotels to include in the input data (80% training data)
    num_hotels = len(hotels)
    num_input_hotels = int(0.8 * num_hotels)

    # Select the first 80% of hotels for the input (training) data
    input_hotels = hotels[:num_input_hotels]
    # Select the remaining 20% of hotels for the test data
    test_hotels = hotels[num_input_hotels:]

    # Convert hotel information to input tensor
    training_data = torch.tensor([hotel.to_tensor() for hotel in input_hotels])
    test_data = torch.tensor([hotel.to_tensor() for hotel in test_hotels])
    return training_data, test_data

# Train the recommender system
def train_recommender_system(input_data: torch.Tensor, num_epochs: int, component: str):
    # Convert input_data and target_data into TensorDataset
    X = input_data[:, :-1]
    #print(X.shape)
    y = input_data[:, -1]
    #print(y.shape)
    # dataset = TensorDataset(input_data[:, :-1], input_data[:, -1])
    dataset = TensorDataset(X, y)

    # Create a DataLoader to split the dataset into batches
    batch_size = 64
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    #print(dataset)
    # input_size = input_data.shape[1]
    input_size = X.shape[1]
    # output_size = target_data.shape[1]
    output_size = 1
    hidden_size = 64

    model = RecommenderSystem(input_size, hidden_size, output_size)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(num_epochs):
        for x_batch, y_batch in dataloader:
            optimizer.zero_grad()
            output = model(x_batch)
            # print("Output: ", output)
            # print("Y_batch: ", y_batch)
            loss = criterion(output, y_batch)
            loss.backward()
            optimizer.step()

        if (epoch+1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}")

    # Save the trained model
    save_file = f'trained_model_{component}.pth'
    torch.save(model.state_dict(), save_file)


# Define target data for training (e.g., another flight recommendation)

# # Load flight data from the Flight table
# flights = load_flight_data()
# # Prepare input data for training the recommender system
# input_data, target_data = prepare_flight_data(flights)


# # Train the recommender system
# num_epochs = 100
# train_recommender_system(input_data, target_data, num_epochs)


def generate_flight_recommendations(flight: schema.FlightModel) -> List[schema.FlightModel]:
    # Prepare input data for the given flight
    input_data = encode_flight_data([flight])
    input_data = torch.tensor(input_data, dtype=torch.float32)
    X = input_data[:, :-1]

    # Load the trained model
    model = RecommenderSystem(X.shape[1], 64, 1)
    model.load_state_dict(torch.load('trained_model_flight.pth'))

    # Generate recommendations
    with torch.no_grad():
        recommendations = model(X)

    # Convert recommendations to Flight objects
    recommended_flights = []
    for recommendation in recommendations:
        recommended_flights.append(recommendation[0].item())  # Extract the value from the tensor

    return recommended_flights

def generate_hotel_recommendations(hotel: HotelModel.Hotel) -> List[HotelModel.Hotel]:
    # Prepare input data for the given hotel
    input_data = prepare_hotel_data([hotel])

    # Load the trained model
    model = RecommenderSystem(input_data.shape[1], 64, input_data.shape[1])
    model.load_state_dict(torch.load('trained_model_hotel.pth'))

    # Generate recommendations
    with torch.no_grad():
        recommendations = model(input_data)

    # Convert recommendations to Hotel objects
    recommended_hotels = []
    for recommendation in recommendations:
        recommended_hotels.append(HotelModel.Hotel.from_tensor(recommendation))

    return recommended_hotels




