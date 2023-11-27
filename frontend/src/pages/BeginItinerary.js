import React from "react";
import Select from 'react-select';
import CreatableSelect from 'react-select/creatable';
import "../styles/BeginItinerary.css";
import { useState, useContext } from "react";
import { AuthContext } from "../AuthContext";
import { useNavigate } from "react-router-dom";


function BeginItinerary() {
    const [formData, setFormData] = useState({
        itineraryTitle: "",
        emailList: [],
        destination: "",
        departure: "",
        departureDate: "",
        returnDate: "",
        travelReason: "",
        leisureActivites: "",
        budget: 0
    });

    const navigate = useNavigate();
    const { user } = useContext(AuthContext);
    if (!user) {
        console.log(user)
        navigate("/register");
        return null;
    }


    const createItinerary = async (itineraryTitle, emailList, destination, departure, departureDate, returnDate, travelReason, leisureActivites, budget) => {
        const response = await fetch('http://localhost:8000/itinerary/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                itineraryTitle,
                emailList,
                destination,
                departure,
                departureDate,
                returnDate,
                travelReason,
                leisureActivites,
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
        createItinerary(formData.itineraryTitle, formData.emailList, formData.destination, formData.departure, formData.departureDate, formData.returnDate, formData.travelReason, formData.leisureActivites, formData.budget);

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
                            Departing From: <input
                                type="text"
                                placeholder="Departing from..."
                                value={formData.departure}
                                onChange={(event) =>
                                    setFormData({ ...formData, departure: event.target.value })
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

                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <label style={{ marginRight: '20px' }}>
                                Reason for Travel: <Select
                                    placeholder="Select One"
                                    options={[
                                        { value: 'Leisure', label: 'Leisure' },
                                        { value: 'Business', label: 'Business' },
                                        { value: 'Family', label: 'Family' },
                                        { value: 'Friends', label: 'Friends' },
                                        { value: 'Other', label: 'Other' },
                                    ]}
                                    defaultValue={""}
                                    onChange={(event) => {
                                        setFormData({ ...formData, travelReason: event.value })
                                    }
                                    }
                                />
                            </label>

                            <label>
                                Favorite Activites: <Select
                                    placeholder="Select One"
                                    options={[
                                        { value: 'Resturants and Local Cuisine', label: 'Resturants and Local Cuisine' },
                                        { value: 'Museums', label: 'Museums' },
                                        { value: 'Historical Sites', label: 'Historical Sites' },
                                        { value: 'Shopping', label: 'Shopping' },
                                        { value: 'Amusement Parks', label: 'Amusement Parks' },
                                        { value: 'Nightlife', label: 'Nightlife' },
                                        { value: 'Other', label: 'Other' },
                                    ]}
                                    onChange={(event) => {
                                        setFormData({ ...formData, leisureActivites: event.value })
                                    }
                                    }
                                />
                            </label>
                        </div>
                        <label>
                            Email List: <CreatableSelect
                                isMulti
                                placeholder="Enter email addresses..."
                                onChange={(selectedOptions) => {
                                    const emails = selectedOptions.map(option => option.value);
                                    console.log(emails);
                                    setFormData({ ...formData, emailList: emails });
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
