
import React, { useEffect, useState } from 'react';
import { useAuth } from '../AuthContext';

import '../styles/Itineraries.css';

function Itineraries() {
    const [itineraries, setItineraries] = useState([]);
    const { user } = useAuth(); // Get the current user from your AuthContext

    useEffect(() => {
        // Replace with your actual API endpoint
        fetch(`http://localhost:8000/itinerary/${user.id}`)
            .then(response => response.json())
            .then(data => setItineraries(data));
    }, [user]);

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
                        <th>Creator</th>
                        <th>Members</th>
                        <th>Destination</th>
                        <th>Flight</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <button
                                type="button"
                                class="btn btn-link btn-rounded btn-sm fw-bold"
                                data-mdb-ripple-color="dark"
                            >
                                Edit
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
};

export default Itineraries;
