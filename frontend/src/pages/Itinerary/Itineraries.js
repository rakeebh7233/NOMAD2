
import React, { useEffect, useState } from 'react';
import { useAuth } from '../../AuthContext';
import '../../styles/Itineraries.css';
import RatingModal from './RatingModal';
import { useNavigate } from "react-router-dom";
import { Link } from 'react-router-dom';

function Itineraries() {
    const [itineraries, setItineraries] = useState([]);
    const [pastItineraries, setPastItineraries] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [selectedItinerary, setSelectedItinerary] = useState(null);
    const { user } = useAuth(); // Get the current user from your AuthContext
    const navigate = useNavigate();

    useEffect(() => {
        fetch(`http://localhost:8000/itineraries/${user.id}`)
            .then(response => response.json())
            .then(data => setItineraries(data))
            .catch(error => console.log(error));

        fetch(`http://localhost:8000/itineraries/${user.id}/past`)
            .then(response => response.json())
            .then(data => setPastItineraries(data))
            .catch(error => console.log(error));

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
            setPastItineraries(pastItineraries.filter(itinerary => itinerary.id !== id));

        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleOpenModal = (itinerary) => {
        setSelectedItinerary(itinerary);
        setShowModal(true);
    };

    const handleCloseModal = async () => {
        setSelectedItinerary(null);
        setShowModal(false);

        // Re-fetch the data from the server
        const response = await fetch(`http://localhost:8000/itineraries/${user.id}/past`);
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.statusText}`);
        }
        const data = await response.json();
        setPastItineraries(data);
    };

    function openTab(evt, tabName) {
        // Declare all variables
        var i, tabcontent, tablinks;

        // Get all elements with class="tabcontent" and hide them
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }

        // Get all elements with class="tablinks" and remove the class "active"
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }

        // Show the current tab, and add an "active" class to the button that opened the tab
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";
    }

    return (
        <div class="container" id="itineraries">
            <button type="button" class="btn btn-primary btn-lg">
                <a class="nav-link text-light" href="/itineraries/new">Create New Itinerary</a>
            </button>
            <br />
            <h1>Your Itineraries</h1>
            <div id="tableContainer">
                <div class="tab">
                    <button class="tablinks" onClick={(evt) => openTab(evt, 'currItin')}>Current Itineraries</button>
                    <button class="tablinks" onClick={(evt) => openTab(evt, 'pastItin')}>Past Itineraries</button>
                </div>

                <table id="currItin" class="table align-middle bg-white tabcontent">
                    <thead class="bg-light">
                        <tr>
                            <th>Title</th>
                            <th>Destination</th>
                            <th>Departure Airport</th>
                            <th>Arrival Airport</th>
                            <th>Departure Date</th>
                            <th>Return Date</th>
                            {/* <th>Travel Reason</th>
                            <th>Leisure Activities</th> */}
                            <th>Budget</th>
                            <th>Owner</th>
                            <th>Members</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(itineraries) && itineraries.map((itinerary) => (
                            <tr key={itinerary.id}>
                                <td>
                                    <Link to={`/itineraries/${itinerary.id}`}>
                                        {itinerary.itineraryTitle}
                                    </Link>
                                </td>
                                <td>{itinerary.destination}</td>
                                <td>{itinerary.departureAirport}</td>
                                <td>{itinerary.arrivalAirport}</td>
                                <td>{itinerary.departureDate}</td>
                                <td>{itinerary.returnDate}</td>
                                {/* <td>{itinerary.travelReason}</td>
                                <td>{itinerary.leisureActivities}</td> */}
                                <td>{itinerary.budget}</td>
                                <td>{itinerary.creatorUsername}</td>
                                <td>{itinerary.members.map(member => member.username).join(', ')}</td>
                                <td>
                                    <button
                                        type="button"
                                        class="btn btn-link btn-rounded btn-sm fw-bold"
                                        data-mdb-ripple-color="dark"
                                        onClick={() => navigate('/itineraries/new', { state: { itinerary } })}
                                    >
                                        Edit
                                    </button>
                                    <br />
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

                <table id="pastItin" class="table align-middle bg-white tabcontent">
                    <thead class="bg-light">
                        <tr>
                            <th>Title</th>
                            <th>Destination</th>
                            <th>Departure Airport</th>
                            <th>Arrival Airport</th>
                            <th>Departure Date</th>
                            <th>Return Date</th>
                            {/* <th>Travel Reason</th>
                            <th>Leisure Activities</th> */}
                            <th>Budget</th>
                            <th>Owner</th>
                            <th>Members</th>
                            <th>Actions</th>
                            <th>Rating</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(pastItineraries) && pastItineraries.map((itinerary) => (
                            <tr key={itinerary.id}>
                                <td>
                                    <Link to={`/itineraries/${itinerary.id}`}>
                                        {itinerary.itineraryTitle}
                                    </Link>
                                </td>
                                <td>{itinerary.destination}</td>
                                <td>{itinerary.departureAirport}</td>
                                <td>{itinerary.arrivalAirport}</td>
                                <td>{itinerary.departureDate}</td>
                                <td>{itinerary.returnDate}</td>
                                {/* <td>{itinerary.travelReason}</td>
                                <td>{itinerary.leisureActivities}</td> */}
                                <td>{itinerary.budget}</td>
                                <td>{itinerary.creatorUsername}</td>
                                <td>{itinerary.members.map(member => member.username).join(', ')}</td>
                                <td>
                                    <button
                                        type="button"
                                        class="btn btn-link btn-rounded btn-sm fw-bold"
                                        data-mdb-ripple-color="dark"
                                        onClick={() => navigate('/itineraries/new', { state: { itinerary } })}
                                    >
                                        Edit
                                    </button>
                                    <br />
                                    <button
                                        type="button"
                                        class="btn btn-link btn-rounded btn-sm fw-bold text-danger"
                                        data-mdb-ripple-color="dark"
                                        onClick={() => deleteItinerary(itinerary.id)}
                                    >
                                        Delete
                                    </button>
                                </td>
                                <td>
                                    {itinerary.rating ? (
                                        itinerary.rating
                                    ) : (
                                        <button
                                            onClick={() => handleOpenModal(itinerary)}
                                            type="button"
                                            className="btn btn-link btn-rounded btn-sm fw-bold text-warning"
                                            data-mdb-ripple-color="dark"
                                        >
                                            Rate
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <RatingModal show={showModal} handleClose={handleCloseModal} itinerary_id={selectedItinerary ? selectedItinerary.id : null} />
        </div>
    );
};

export default Itineraries;
