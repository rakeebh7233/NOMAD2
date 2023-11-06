import React from "react";
import Select from 'react-select';
import axios from "axios";
import "../styles/BeginItinerary.css";
import { useEffect, useState } from "react"; 
import { useParams } from "react-router-dom";

function BeginItinerary({addCustomItinerary}) {
    const[itineraryName, setItineraryName] = useState("");
    const[emailList, setEmailList] = useState([]);
    const[destination, setDestination] = useState("");
    const[departure, setDeparture] = useState("");
    const[departureDate, setDepartureDate] = useState("");
    const[returnDate, setReturnDate] = useState("");
    const[travelReason, setTravelReason] = useState([]);
    const[leisureActivites, setLeisureActivities] = useState([]);
    const[budget, setBudget] = useState("");
    const[date, setDate] = useState("");



    const handleSubmit = (e) => {
        e.PreventDefault();
        addCustomItinerary(itineraryName, emailList, destination, departure, departureDate, returnDate, travelReason, leisureActivites, budget);
    };

    const searchCustomComponents = (e) =>{
        console.log("hi");
    }

    return (
        <section id="beginItinPage">
            <form class="flex-form" onSubmit={e => { handleSubmit(e) }}>
            <label>Itinerary Name:</label>
            <br />
            <input 
            name='itineraryName'
            type='text'
            value={itineraryName}
            onChange={e => setItineraryName(e.target.value)}
            />
            <br/>
            <label>Email(s): (seperate by comma)</label>
            <br />
            <input 
            name='emailList'
            type='text' 
            placeholder="email1, email2, email3"
            value={emailList}
            onChange={e => setEmailList(e.target.value)}
            />
            <br />
            <label>Destination:</label>
            <br />
            <input
            name='destination' 
            type='text'
            placeholder= "City, Country"
            value={date}
            onChange={e => setDestination(e.target.value)}
            />
            <br />
            <label>Departing From:</label>
            <br />
            <input 
            name= 'departure'
            type='text'
            value={departure}
            onChange={e => setDeparture(e.target.value)}
            />
            <br />
            <label>Departure Date:</label>
            <br />
            <input
            name= 'departureDate'
            type='date'
            placeholder="YYYY-MM-DD"
            value={departureDate}
            onChange={e => setDepartureDate(e.target.value)}
            />
            <br />
            <label>Return Date:</label>
            <br />
            <input
            name= 'returnDate'
            type='date'
            placeholder="YYYY-MM-DD"
            value={returnDate}
            onChange={e => setReturnDate(e.target.value)}
            />
            <br />
            <label>Reason For Travel:</label>
            <br />
            <Select
                name='travelReason'
                placeholder="Select All that Apply"
                value={travelReason}
                options={[
                    { value: 'Leisure', label: 'Leisure' },
                    { value: 'Business', label: 'Business' },
                    { value: 'Family', label: 'Family' },
                    { value: 'Friends', label: 'Friends' },
                    { value: 'Other', label: 'Other' },
                ]}
                onChange={
                    e => setTravelReason(e.target.value)
                }
                isMulti
            />
            <br />
            <label>Favorite Leisure Activites:</label>
            <br />
            <Select
                name='leisureActivities'
                placeholder="Select All that Apply"
                value={leisureActivites}
                options={[
                    { value: 'Resturants and Local Cuisine', label: 'Resturants and Local Cuisine' },
                    { value: 'Museums', label: 'Museums' },
                    { value: 'Historical Sites', label: 'Historical Sites' },
                    { value: 'Shopping', label: 'Shopping' },
                    { value: 'Amusement Parks', label: 'Amusement Parks' },
                    { value: 'Nightlife', label: 'Nightlife' },
                    { value: 'Other', label: 'Other' },
                ]}
                onChange={
                    e => setTravelReason(e.target.value)
                }
                isMulti
            />
            <br/>
            <button id="beginButton" onClick={searchCustomComponents}> TO YOUR NEXT ADVENTURE </button>
      </form>
        </section>
        
    );

}

export default BeginItinerary

