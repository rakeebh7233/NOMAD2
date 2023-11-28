import sys 
sys.path.append("..")
from models import FlightModel, HotelModel
from fastapi import Depends
import schema, database
from sqlalchemy.orm import Session
from typing import List

import torch
import random
import torch.nn as nn
import torch.optim as optim

get_db = database.get_db

# Define the recommender system model
class RecommenderSystem(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RecommenderSystem, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Load flight data from the Flight table
def load_flight_data(db: Session = Depends(get_db)) -> List[FlightModel.Flight]:
    flights = db.query(FlightModel).all()
    return flights

# Load hotel data from the Hotel table
def load_hotel_data(db: Session = Depends(get_db)) -> List[HotelModel.Hotel]:
    hotels = db.query(HotelModel).all()
    return hotels

# Prepare flight input data for training the recommender system
def prepare_flight_data(flights: List[FlightModel.Flight]) -> torch.Tensor:
    # Calculate the number of flights to include in the input data (80% training data)
    num_flights = len(flights)
    num_input_flights = int(0.8 * num_flights)

    # Select the first 80% of flights for the input (training) data
    input_flights = flights[:num_input_flights]
    # Select the remaining 20% of flights for the test data
    test_flights = flights[num_input_flights:]

    # Convert flight information to input tensor
    training_data = torch.tensor([flight.to_tensor() for flight in input_flights])
    test_data = torch.tensor([flight.to_tensor() for flight in test_flights])
    return training_data, test_data

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
def train_recommender_system(input_data: torch.Tensor, target_data: torch.Tensor, num_epochs: int, component: str):
    input_size = input_data.shape[1]
    output_size = target_data.shape[1]
    hidden_size = 64

    model = RecommenderSystem(input_size, hidden_size, output_size)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(num_epochs):
        optimizer.zero_grad()
        output = model(input_data)
        loss = criterion(output, target_data)
        loss.backward()
        optimizer.step()

        if (epoch+1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}")

    # Save the trained model
    save_file = 'trained_model_{name}.pth'.format(name=component)
    torch.save(model.state_dict(), 'trained_model.pth')


# Define target data for training (e.g., another flight recommendation)

# # Load flight data from the Flight table
# flights = load_flight_data()
# # Prepare input data for training the recommender system
# input_data, target_data = prepare_flight_data(flights)


# # Train the recommender system
# num_epochs = 100
# train_recommender_system(input_data, target_data, num_epochs)


def generate_flight_recommendations(flight: FlightModel.Flight) -> List[FlightModel.Flight]:
    # Prepare input data for the given flight
    input_data = prepare_flight_data([flight])

    # Load the trained model
    model = RecommenderSystem(input_data.shape[1], 64, input_data.shape[1])
    model.load_state_dict(torch.load('trained_model.pth'))

    # Generate recommendations
    with torch.no_grad():
        recommendations = model(input_data)

    # Convert recommendations to Flight objects
    recommended_flights = []
    for recommendation in recommendations:
        recommended_flights.append(FlightModel.Flight.from_tensor(recommendation))

    return recommended_flights

def generate_hotel_recommendations(hotel: HotelModel.Hotel) -> List[HotelModel.Hotel]:
    # Prepare input data for the given hotel
    input_data = prepare_hotel_data([hotel])

    # Load the trained model
    model = RecommenderSystem(input_data.shape[1], 64, input_data.shape[1])
    model.load_state_dict(torch.load('trained_model.pth'))

    # Generate recommendations
    with torch.no_grad():
        recommendations = model(input_data)

    # Convert recommendations to Hotel objects
    recommended_hotels = []
    for recommendation in recommendations:
        recommended_hotels.append(HotelModel.Hotel.from_tensor(recommendation))

    return recommended_hotels




