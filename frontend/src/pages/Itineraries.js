
import React, { useEffect, useState } from 'react';
import { useAuth } from '../AuthContext';

import '../styles/Itineraries.css';

function Itineraries() {
    const [itineraries, setItineraries] = useState([]);
    const { user } = useAuth(); // Get the current user from your AuthContext

    useEffect(() => {
        // Replace with your actual API endpoint
        fetch(`http://localhost:8000/itineraries/${user.id}`)
            .then(response => response.json())
            .then(data => setItineraries(data));
    }, [user]);

    const deleteItinerary = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/itineraries/${id}`, {
                method: 'DELETE',
            });
            if (!response.ok) {
                throw new Error(`An error occurred: ${response.statusText}`);
            }
    
            // Remove the deleted itinerary from the local state
            setItineraries(itineraries.filter(itinerary => itinerary.id !== id));
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div class="container" id="itineraries">
            <button type="button" class="btn btn-primary btn-lg">
                <a class="nav-link text-light" href="/itineraries/new">Create New Itinerary</a>
            </button>
            <h1>View Itineraries</h1>
            <table class="table align-middle bg-white">
                <thead class="bg-light">
                    <tr>
                        <th>Title</th>
                        <th>Destination</th>
                        <th>Departure</th>
                        <th>Departure Date</th>
                        <th>Return Date</th>
                        <th>Travel Reason</th>
                        <th>Leisure Activities</th>
                        <th>Budget</th>
                        <th>Creator_ID</th>
                        <th>Members</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {Array.isArray(itineraries) && itineraries.map((itinerary) => (
                        <tr key={itinerary.id}>
                            <td>{itinerary.itineraryTitle}</td>
                            <td>{itinerary.destination}</td>
                            <td>{itinerary.departure}</td>
                            <td>{itinerary.departureDate}</td>
                            <td>{itinerary.returnDate}</td>
                            <td>{itinerary.travelReason}</td>
                            <td>{itinerary.leisureActivities}</td>
                            <td>{itinerary.budget}</td>
                            <td>{itinerary.creator_id}</td>
                            <td>{itinerary.members.map(member => member.username).join(', ')}</td>
                            <td>
                                <button
                                    type="button"
                                    class="btn btn-link btn-rounded btn-sm fw-bold"
                                    data-mdb-ripple-color="dark"
                                >
                                    Edit
                                </button>
                                <button
                                    type="button"
                                    class="btn btn-link btn-rounded btn-sm fw-bold text-danger"
                                    data-mdb-ripple-color="dark"
                                    onClick={() => deleteItinerary(itinerary.id)}
                                >
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Itineraries;
