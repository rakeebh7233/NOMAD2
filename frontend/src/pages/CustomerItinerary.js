import React from "react";
import Select from 'react-select';
import axios from "axios";
import "../styles/CustomItin.css";
import { useParams } from "react-router-dom";
import { useContext, useState, useEffect } from "react";
import { AuthContext } from "../AuthContext";
import { Navigate } from "react-router-dom";


function CustomerItinerary() {
    const { itinerary_id } = useParams();
    const [hotels, setHotels] = useState([]);


    const [restaurants, setRestaurants] = useState([]);
    const [myRestaurants, setMyRestaurants] = useState([]);

    const [flights, setFlights] = useState([]);

    useEffect(() => {
        getRestaurants();
        getHotels();
        getFlights();
        getMyRestaurants();

    }, []);

    const { user } = useContext(AuthContext);

    // If the user is not logged in, redirect to the login page
    if (!user) {
        return <Navigate to="/register" />;
    }

    const getSuggestions = () => {
        //make calls to suggestions
    };

    const setPlannedSection = () => {
        //setThingsAsNeeded
    }

    const getHotels = async () => {

        const geoID = localStorage.getItem('BookingAPIGeoID');
        const startDate = localStorage.getItem('startDate');
        const endDate = localStorage.getItem('endDate');

        const options = {
            method: 'GET',
            url: 'http://127.0.0.1:8000/hotel/hotel_internal/' + geoID + '/' + startDate + '/' + endDate + '/2/1',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
        };

        try {
            axios.request(options).then((data) => {
                if (data['data'].length === 0) {
                    const options1 = {
                        method: 'GET',
                        url: 'http://127.0.0.1:8000/hotel/hotel_external/' + geoID + '/' + startDate + '/' + endDate + '/2/1',
                        headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
                    };
                    try {
                        axios.request(options1).then((data1) => {
                            setHotels(data1.data);
                        })
                    }
                    catch (error) {
                        console.error(error)
                    }
                }
                else {
                    setHotels(data.data);
                }

            });
        } catch (error) {
            console.error(error);
        }
    }

    const getFlights = async () => {
        const startDate = localStorage.getItem('startDate');
        const endDate = localStorage.getItem('endDate');

        const flightList = [];

        const options = {
            method: 'GET',
            url: 'http://127.0.0.1:8000/flight/internal_search/round/JFK/LAX/' + startDate + '/' + startDate + '/{search}?cabinClass=ECONOMY',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
        }
        try {
            axios.request(options).then((data) => {
                if (data['data'].length !== 0) {
                    const options1 = {
                        method: 'GET',
                        url: 'http://127.0.0.1:8000/flight/internal_search/round/LAX/JFK/' + endDate + '/' + endDate + '/{search}?cabinClass=ECONOMY',
                        headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
                    }
                    try {
                        axios.request(options1).then((data1) => {
                            if (data1['data'].length !== 0) {
                                for (let i = 0; i < data['data'].length; i++) {
                                    flightList.push(data['data'][i]);
                                }
                                for (let i = 0; i < data1['data'].length; i++) {
                                    flightList.push(data1['data'][i]);
                                }
                                setFlights(flightList)
                            }
                            else {
                                const options2 = {
                                    method: 'GET',
                                    url: 'http://127.0.0.1:8000/flight/external_search/round/JFK.AIRPORT/LAX.AIRPORT/' + startDate + '/' + endDate + '/ECONOMY',
                                    headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
                                }
                                try {
                                    axios.request(options2).then((data) => {
                                        for (let i = 0; i < data.length; i++) {
                                            flightList.push(data[i]);
                                        }
                                        setFlights(flightList);
                                    })
                                }
                                catch (error) {
                                    console.error(error)
                                }
                            }
                        })
                    }
                    catch (error) {
                        console.error(error)
                    }
                }
                else {
                    const options2 = {
                        method: 'GET',
                        url: 'http://127.0.0.1:8000/flight/external_search/round/JFK.AIRPORT/LAX.AIRPORT/' + startDate + '/' + endDate + '/ECONOMY',
                        headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
                    }
                    try {
                        axios.request(options2).then((data) => {
                            for (let i = 0; i < data.length; i++) {
                                flightList.push(data[i]);
                            }
                            setFlights(flightList);
                        })
                    }
                    catch (error) {
                        console.error(error)
                    }
                }
            })
        }
        catch (error) {
            console.error(error)
        }

    }

    const getRestaurants = async () => {
        const geoID = localStorage.getItem('tripAdvisorGeoID')
        const options = {
            method: 'GET',
            url: 'http://127.0.0.1:8000/restaurant/tripadvisorRestaurantLocCheck/{locationId}?locId=' + geoID,
        };

        axios.request(options).then((response) => {
            if (response['data']['isInDB']) {
                const options1 = {
                    method: 'GET',
                    url: 'http://127.0.0.1:8000/restaurant/' + geoID,
                };
                axios.request(options1).then((response1) => {
                    setRestaurants(response1['data']);
                });
            }
            else {
                const options2 = {
                    method: 'GET',
                    url: 'http://127.0.0.1:8000/restaurant/tripadvisorSearch/' + geoID,
                };
                axios.request(options2).then((response1) => {
                    setRestaurants(response1['data']);
                })
            }
        })
    }

    const getMyRestaurants = async () => {
        const response = await fetch(`http://localhost:8000/itineraries/${itinerary_id}/restaurants`);
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.statusText}`);
        }
        const data = await response.json();
        setMyRestaurants(data);
    }

    const addRestaurant = async (restaurant_id, restaurantName) => {
        const geoID = localStorage.getItem('tripAdvisorGeoID')
        const response = await fetch('http://localhost:8000/restaurant_booking/new_booking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                geoID: geoID,
                restaurant_id: restaurant_id,
                itinerary_id: itinerary_id,
                restaurantName: restaurantName
            })
        });

        if (response.ok) {
            console.log("Added restaurant")
        } else {
            throw new Error("Restaurant not added");
        }

        const data = await response.json();
        return data;
    }

    return (
        <section id="customItinPage">
            <div className="row gx-1 px-4">

                <div className="planned-container col-sm-6">
                    <h1>Planned</h1>
                    <h2>Hotel</h2>
                    <div className="card-container">
                        <img
                            src="https://img.freepik.com/free-photo/beautiful-luxury-outdoor-swimming-pool-hotel-resort_74190-7433.jpg"
                            alt="Card"
                            className="card-img"
                        />
                        <h3 className="card-title">Hilton</h3>
                        <div className="card-description">Hotel-Address: NYU Tandon School of Engineering</div>
                        <a href="this should go to hotel booking link" className="card-btn">Booking</a>
                    </div>

                    <h2>Flight</h2>

                    <div className="card-container">
                        <img
                            src="https://petapixel.com/assets/uploads/2022/05/how-to-take-photos-out-of-an-airplane-window-featured.jpg"
                            alt="Card"
                            className="card-img"
                        />
                        <h3 className="card-title">Delta Airline</h3>
                        <div className="card-description">Airport: LGA</div>
                        <a href="this should go to hotel booking link" className="card-btn">Booking</a>
                    </div>

                    <h2>Activites</h2>
                    <div className="d-flex">
                        <div className="card-container">
                            <img
                                src="https://images.ctfassets.net/0wjmk6wgfops/nb3Q0W8VmjzthrOMiSzPt/6b8bf6ccb00141d84d32829455d073a9/Skier_resize_AdobeStock_617199939.jpeg?q=70"
                                alt="Card"
                                className="card-img"
                            />
                            <h3 className="card-title">Skiing</h3>
                            <div className="card-description">Day: October 30th, 2023</div>
                            <a href="this should go to hotel booking link" className="card-btn">Booking</a>
                        </div>
                        <div className="card-container">
                            <img
                                src="https://media-cldnry.s-nbcnews.com/image/upload/t_fit-1500w,f_auto,q_auto:best/newscms/2017_45/2222291/171110-jet-engine-power-suit-air-njs-213p.jpg"
                                alt="Card"
                                className="card-img"
                            />
                            <h3 className="card-title">Jet Packing</h3>
                            <div className="card-description">Day: November 2nd, 2023</div>
                            <a href="this should go to hotel booking link" className="card-btn">Booking</a>
                        </div>
                    </div>

                    <h2>Restaurants</h2>
                    <div className="d-flex flex-wrap">
                        {myRestaurants.map((rest) => (
                            <div className="card-container" key={rest.id}>
                                <img
                                    src={rest.image_url}
                                    alt="Card"
                                    className="card-img"
                                />
                                <h3 className="card-title">{rest.restaurant.name}</h3>
                                <div className="card-description">{rest.restaurant.description}</div>
                                <a href={rest.restaurant.booking_link} className="card-btn">Booking</a>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="suggested-container col-sm-6">
                    <h1>Suggested</h1>
                    <h2>Hotel</h2>

                    <div className="cards d-flex">
                        {hotels.map(rest => (
                            <div className="card-container">
                                <img
                                    src="https://monicafrancis.com/wp-content/uploads/2021/12/Monica-Francis-Best-NYC-Restaurants-La-Mercerie.jpg"
                                    alt="Card"
                                    className="card-img"
                                />
                                <div className="d-flex">
                                    <h3 className="card-title">{rest.name}</h3>
                                </div>
                                <div className="card-description">Total Price: {rest.totalPrice}</div>
                                <div className="card-description">Guests: {rest.guests}  Rooms: {rest.rooms}</div>
                                <a className="primary-btn">Add to Itinerary</a>
                                <a href="https://www.booking.com" target="_blank" className="card-btn">View </a>
                            </div>
                        ))}

                    </div>

                    <h2>Flight</h2>
                    <div className="cards d-flex">
                        {flights.map(flight => (
                            <div className="card-container">
                                <img
                                    src="https://petapixel.com/assets/uploads/2022/05/how-to-take-photos-out-of-an-airplane-window-featured.jpg"
                                    alt="Card"
                                    className="card-img"
                                />
                                <div className="d-flex">
                                    <h3 className="card-title">{flight.carrier}</h3>
                                </div>
                                <div className="card-description">Departure Airport: {flight.departureAirport}  Arrival Airport: {flight.arrivalAirport}</div>
                                <div className="card-description">Cabin: {flight.cabinClass} </div>
                                <div className="card-description">Cost : {flight.totalPrice}</div>
                                <a className="primary-btn">Add to Itinerary</a>
                                <a href="https://www.booking.com" target="_blank" className="card-btn">View </a>
                            </div>
                        ))}
                    </div>

                    <h2>Activites</h2>
                    <div className="cards d-flex">
                        <div className="card-container">
                            <img
                                src="https://images.ctfassets.net/0wjmk6wgfops/nb3Q0W8VmjzthrOMiSzPt/6b8bf6ccb00141d84d32829455d073a9/Skier_resize_AdobeStock_617199939.jpeg?q=70"
                                alt="Card"
                                className="card-img"
                            />
                            <h3 className="card-title">Skiing</h3>
                            <div className="card-description">Day: October 30th, 2023</div>
                            <a className="primary-btn">Add to Itinerary</a>
                            <a href="this should go to hotel booking link" className="card-btn">Booking</a>
                        </div>
                        <div className="card-container">
                            <img
                                src="https://media-cldnry.s-nbcnews.com/image/upload/t_fit-1500w,f_auto,q_auto:best/newscms/2017_45/2222291/171110-jet-engine-power-suit-air-njs-213p.jpg"
                                alt="Card"
                                className="card-img"
                            />
                            <h3 className="card-title">Jet Packing</h3>
                            <div className="card-description">Day: November 2nd, 2023</div>
                            <a className="primary-btn">Add to Itinerary</a>
                            <a href="this should go to hotel booking link" className="card-btn">Booking</a>
                        </div>
                    </div>

                    <h2>Restaurants</h2>
                    <div className="cards d-flex">
                        {restaurants.map(rest => (
                            <div className="card-container">
                                <img
                                    src="https://monicafrancis.com/wp-content/uploads/2021/12/Monica-Francis-Best-NYC-Restaurants-La-Mercerie.jpg"
                                    alt="Card"
                                    className="card-img"
                                />
                                <div className="d-flex">
                                    <h3 className="card-title">{rest.name}</h3>
                                </div>
                                <div className="card-description">Price Tag: {rest.priceTag}</div>
                                <div className="card-description">Avg Rating: {rest.averageRating}</div>
                                <a className="primary-btn" onClick={() => addRestaurant(rest.id, rest.name)}>Add to Itinerary</a>
                                <a href={rest.menuURL} className="card-btn">Menu</a>
                            </div>
                        ))}

                    </div>

                </div>
            </div>



        </section>
    );
}

export default CustomerItinerary