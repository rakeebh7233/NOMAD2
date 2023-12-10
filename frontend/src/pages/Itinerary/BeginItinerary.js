import React from "react";
import Select from 'react-select';
import CreatableSelect from 'react-select/creatable';
import "../../styles/BeginItinerary.css";
import { useState, useContext, useEffect } from "react";
import { AuthContext } from "../../AuthContext";
import { useNavigate, useLocation } from "react-router-dom";


function BeginItinerary() {
    const [formData, setFormData] = useState({
        itineraryTitle: "",
        members: [],
        destination: "",
        departureAirport: "",
        arrivalAirport: "",
        departureDate: "",
        returnDate: "",
        budget: 0
    });

    const navigate = useNavigate();
    const location = useLocation();
    const { user } = useContext(AuthContext);

    const itinerary = location.state?.itinerary;

    useEffect(() => {
        if (itinerary) {
            setFormData({
                itineraryTitle: itinerary.itineraryTitle,
                members: itinerary.members,
                destination: itinerary.destination,
                departureAirport: itinerary.departureAirport,
                arrivalAirport: itinerary.arrivalAirport,
                departureDate: itinerary.departureDate,
                returnDate: itinerary.returnDate,
                budget: itinerary.budget
            });
        }
    }, [itinerary]);

    if (!user) {
        console.log(user)
        navigate("/register");
        return null;
    }


    const createItinerary = async (itineraryTitle, members, destination, departureAirport, arrivalAirport, departureDate, returnDate, budget) => {
        const url = itinerary ? `http://localhost:8000/itineraries/${itinerary.id}` : 'http://localhost:8000/itineraries/create';
        const method = itinerary ? 'PUT' : 'POST';

        console.log(departureDate)
        console.log(returnDate)
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                itineraryTitle,
                members,
                destination,
                departureAirport,
                arrivalAirport,
                departureDate,
                returnDate,
                budget,
                creator_id: user.id
            }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        } else {
            navigate("/itineraries");
        }

        const itineraryData = await response.json();
        return itineraryData;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formData)
        createItinerary(formData.itineraryTitle, formData.members, formData.destination, formData.departureAirport, formData.arrivalAirport, formData.departureDate, formData.returnDate, formData.budget);
    };


    return (
        <div className="form">
            <div className="beginItinHeader">
                <h1>Your Next Adventure Awaits...</h1>
            </div>
            <div className="form-container1">
                <div className="body">
                    <div className="itinerary-container">
                        <label>
                            Itinerary Name: <input
                                type="text"
                                placeholder="Name..."
                                value={formData.itineraryTitle}
                                onChange={(event) =>
                                    setFormData({ ...formData, itineraryTitle: event.target.value })
                                }
                            />
                        </label>

                        <label>
                            Destination: <input
                                type="text"
                                placeholder="Destination..."
                                value={formData.destination}
                                onChange={(event) =>
                                    setFormData({ ...formData, destination: event.target.value })
                                }
                            />
                        </label>

                        <label>
                            Departure Airport: <input
                                type="text"
                                placeholder="Departing from..."
                                value={formData.departureAirport}
                                onChange={(event) =>
                                    setFormData({ ...formData, departureAirport: event.target.value })
                                }
                            />
                        </label>

                        <label>
                            Arrival Airport: <input
                                type="text"
                                placeholder="Departing from..."
                                value={formData.arrivalAirport}
                                onChange={(event) =>
                                    setFormData({ ...formData, arrivalAirport: event.target.value })
                                }
                            />
                        </label>

                        <label>
                            Departure Date: <input
                                type="date"
                                placeholder="MM/DD/YYY"
                                value={formData.departureDate}
                                onChange={(event) =>
                                    setFormData({ ...formData, departureDate: event.target.value })
                                }
                            />
                        </label>

                        <label>
                            Return Date: <input
                                type="date"
                                placeholder="MM/DD/YYYY"
                                value={formData.returnDate}
                                onChange={(event) =>
                                    setFormData({ ...formData, returnDate: event.target.value })
                                }
                            />
                        </label>

                        <label>
                            Budget: <input
                                type="number"
                                placeholder="$"
                                value={formData.budget}
                                onChange={(event) =>
                                    setFormData({ ...formData, budget: event.target.value })
                                }
                            />
                        </label>

        
                        <label>
                            Email List: <CreatableSelect
                                isMulti
                                placeholder="Enter email addresses..."
                                onChange={(selectedOptions) => {
                                    const emails = selectedOptions.map(option => option.value);
                                    console.log(emails);
                                    setFormData({ ...formData, members: emails });
                                }}
                            />
                        </label>
                    </div>
                </div>
                <div style={{ marginTop: '10px' }} className="footer">
                    <button onClick={handleSubmit} >Submit</button>
                </div>
            </div>
        </div>

    );

}

export default BeginItinerary
