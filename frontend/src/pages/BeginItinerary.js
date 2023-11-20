import React from "react";
import Select from 'react-select';
import "../styles/BeginItinerary.css";
import { useEffect, useState, useContext } from "react";
import { AuthContext } from "../AuthContext";
import { Navigate } from "react-router-dom";


function BeginItinerary() {
    const [formData, setFormData] = useState({
        itineraryTitle: "",
        emailList: "",
        destination: "",
        departure: "",
        departureDate: "",
        returnDate: "",
        travelReason: [],
        leisureActivites: "",
        budget: ""
    })

    const { user } = useContext(AuthContext);
    if (!user) {
        console.log(user)
        return <Navigate to="/register" />;
    }

    const createItinerary = async (itineraryName, emailList, destination, departure, departureDate, returnDate, travelReason, leisureActivites, budget) => {
        const response = await fetch('http://localhost:8000/create_itinerary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                itineraryName,
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
        }
    
        const itineraryData = await response.json();
        return itineraryData;
    };
    

    const handleSubmit = (e) => {
        //e.PreventDefault();
        console.log(formData)
        createItinerary(formData.itineraryName, formData.emailList, formData.destination, formData.departure, formData.departureDate, formData.returnDate, formData.travelReason, formData.leisureActivites, formData.budget);
    };

    const searchCustomComponents = (e) => {
        console.log("hi");
    }

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
                            Email List: <input
                                type="text"
                                placeholder="email1,email2,email3..."
                                value={formData.emailList}
                                onChange={(event) =>
                                    setFormData({ ...formData, emailList: event.target.value })
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
                            Reason for Travel: <Select
                                placeholder="Select All that Apply"
                                options={[
                                    { value: 'Leisure', label: 'Leisure' },
                                    { value: 'Business', label: 'Business' },
                                    { value: 'Family', label: 'Family' },
                                    { value: 'Friends', label: 'Friends' },
                                    { value: 'Other', label: 'Other' },
                                ]}
                                defaultValue={""}
                                onChange={(event) => {
                                    let list = [];
                                    for (let i = 0; i < event.length; i++) {
                                        list.push(event[i].value)
                                    }
                                    setFormData({ ...formData, travelReason: list })
                                }
                                }
                                isMulti
                            />
                        </label>

                        <label>
                            Favorite Activites: <Select
                                placeholder="Select All that Apply"
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
                                    let list = [];
                                    for (let i = 0; i < event.length; i++) {
                                        list.push(event[i].value)
                                    }
                                    setFormData({ ...formData, leisureActivites: list })
                                }
                                }
                                isMulti
                            />
                        </label>

                    </div>
                </div>
                <div className="footer">
                    <button onClick={handleSubmit} >Submit</button>
                </div>
            </div>
        </div>

    );

}

export default BeginItinerary
