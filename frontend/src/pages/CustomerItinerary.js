import React, { useReducer } from "react";
import axios from "axios";
import "../styles/CustomItin.css";
import { useParams } from "react-router-dom";
import { useContext, useState, useEffect } from "react";
import { AuthContext } from "../AuthContext";
import { Navigate, Link } from "react-router-dom";


function CustomerItinerary() {
    const { itinerary_id } = useParams();
    const [hotels, setHotels] = useState([]);
    const [myHotels, setMyHotels] = useState([]);
    const [restaurants, setRestaurants] = useState([]);
    const [myRestaurants, setMyRestaurants] = useState([]);
    const [flights, setFlights] = useState([]);
    const [myFlights, setMyFlights] = useState([]);


    const [destination, setDestination] = useState('');
    const [departureAirport, setDeparture] = useState('');
    const [arrivalAirport, setArrival] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [tripAdvisorGeoID, setTripAdvisorID] = useState('');
    const [bookingGeoID, setBookingGeoID] = useState('');

    const [ignored, forceUpdate] = useReducer(x => x + 1, 0);
    const { user } = useContext(AuthContext);


    useEffect(() => {

        const itinData = async () => {

            const response = await fetch(`http://127.0.0.1:8000/itineraries/currItin/{itinerary_id}?itin_id=${itinerary_id}`)
            const data = await response.json();

            setDestination(data[0].destination);
            setDeparture(data[0].departureAirport);
            setArrival(data[0].arrivalAirport);
            setStartDate(data[0].departureDate);
            setEndDate(data[0].returnDate);

            getLocations(data[0].destination);
            getMyRestaurants();
            getMyFlights();
            getMyHotels();
        }
        itinData();
    }, [ignored]);

    // If the user is not logged in, redirect to the login page
    if (!user) {
        return <Navigate to="/register" />;
    }

    const getLocations = (dest) => {
        const options = {
            method: 'GET',
            url: 'http://127.0.0.1:8000/restaurant/tripadvisorCityCheck/' + dest,
        };

        try {
            axios.request(options).then((response) => {
                if (response['data']['isInDB']) {
                    setTripAdvisorID(response['data']['geoID']);
                    getRestaurants(response['data']['geoID']);
                }
                else {
                    const options1 = {
                        method: 'GET',
                        url: 'http://127.0.0.1:8000/restaurant/locations/' + dest,

                    };

                    try {
                        axios.request(options1).then((response1) => {
                            setTripAdvisorID(response1['data']['geoId']);
                            getRestaurants(response['data']['geoID']);
                        })
                    }
                    catch (error) {
                        console.log(error)
                    }
                }
            });
        } catch (error) {
            console.error(error);
        }

        const options3 = {
            method: 'GET',
            url: 'http://127.0.0.1:8000/hotel/location_internal/' + dest,
            headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
        }

        try {
            axios.request(options3).then((response2) => {
                if (response2['data']['isInDB']) {
                    setBookingGeoID(response2['data']['geoId']);
                }
                else {
                    const options4 = {
                        method: 'GET',
                        url: 'http://127.0.0.1:8000/hotel/location_external/' + dest,
                        headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
                    }

                    try {
                        axios.request(options4).then((response3) => {
                            setBookingGeoID(response3['data']['geoId']);
                        });
                    }
                    catch (error) {
                        console.error(error)
                    }
                }
            });
        }
        catch (error) {
            console.error(error)
        }
    }

    const getSuggestions = (id, type, data) => {
        //make calls to suggestions
        if (type === 'flight') {
            const option = {
                method: 'GET',
                url: 'http://127.0.0.1:8000/flight/suggestions/' + id
            }
            try {
                axios.request(option).then((response) => {
                    let flightData = response['data'];
                    flightData = flightData.filter(val => {
                        for(let i =0; i < data.length; i++){
                            if(val['id'] === data[i]['flight_id']){
                                return false;
                            }
                        }
                        return true;
                    })
                    setFlights(flightData)
                })
            }
            catch (error) {
                console.error(error)
            }
        }
        if (type === 'hotel') {
            const option1 = {
                method: 'GET',
                url: 'http://127.0.0.1:8000/hotel/suggestions/' + id
            }
            try {
                axios.request(option1).then((response) => {
                    let hotelData = response['data'];
                    hotelData = hotelData.filter(val => {
                        for(let i =0; i < data.length; i++){
                            if(val['id'] === data[i]['hotel_id']){
                                return false;
                            }
                        }
                        return true;
                    })
                    setHotels(hotelData)
                })
            }
            catch (error) {
                console.error(error)
            }
        }
    };

    const setPlannedSection = () => {
        //setThingsAsNeeded
    }

    const getMyHotels = async () => {
        const response = await fetch(`http://localhost:8000/itineraries/${itinerary_id}/hotels`);
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.statusText}`);
        }
        const data = await response.json();
        setMyHotels(data);
        if (data.length > 0) {
            getSuggestions(data[0]['hotel_id'], 'hotel', data)
        }
    }

    const removeMyHotel = async (hotel_id) => {
        const response = await fetch(`http://localhost:8000/hotel_booking/delete/${hotel_id}/${itinerary_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        forceUpdate();
    }

    const addHotel = async (hotel_id) => {
        const response = await fetch('http://localhost:8000/hotel_booking/new_booking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                hotel_id: hotel_id,
                itinerary_id: itinerary_id
            })
        });
        forceUpdate();
    }

    const getMyFlights = async () => {
        const response = await fetch(`http://localhost:8000/itineraries/${itinerary_id}/flights`);
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.statusText}`);
        }
        const data = await response.json();
        setMyFlights(data);

        if (data.length > 0) {
            getSuggestions(data[0]['flight_id'], 'flight', data);
        }
    }

    const removeMyFlight = async (flight_id) => {
        const response = await fetch(`http://localhost:8000/flight_booking/delete/${flight_id}/${itinerary_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        forceUpdate();
    }

    const addFlight = async (flight_id) => {
        const response = await fetch('http://localhost:8000/flight_booking/new_booking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                flight_id: flight_id,
                itinerary_id: itinerary_id
            })
        });

        if (response.ok) {
            console.log("Added flight")
        } else {
            throw new Error("Flight not added");
        }
        forceUpdate();
    }

    const getRestaurants = (geoID) => {
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
                    let restaurantData = response1['data'];
                    restaurantData = restaurantData.filter(val => {
                        for(let i =0; i < myRestaurants.length; i++){
                            if(val['id'] === myRestaurants[i]['restaurant_id']){
                                return false;
                            }
                        }
                        return true;
                    })
                    setRestaurants(restaurantData);
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

    const removeMyRestaurant = async (restaurant_id) => {
        const response = await fetch(`http://localhost:8000/restaurant_booking/delete/${restaurant_id}/${itinerary_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        await getMyRestaurants();
        forceUpdate();
    }

    const addRestaurant = async (restaurant_id, restaurantName) => {
        const response = await fetch('http://localhost:8000/restaurant_booking/new_booking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                geoID: tripAdvisorGeoID,
                restaurant_id: restaurant_id,
                itinerary_id: itinerary_id,
                restaurantName: restaurantName
            })
        });
        console.log(response)

        if (response.ok) {
            console.log("Added restaurant")
        } else {
            throw new Error("Restaurant not added");
        }
        await getMyRestaurants();
        console.log(myRestaurants)
        getRestaurants(tripAdvisorGeoID);
        forceUpdate();
    }

    return (
        <section id="customItinPage">
            <div className="row gx-1 px-4">
                <div className="planned-container col-sm-6">
                    <h1>Planned</h1>
                    <h2>Hotel</h2>
                    {myHotels.length === 0 ? (
                        <p style={{ fontStyle: 'italic' }}>Add a Hotel to your itinerary</p>
                    ) : (
                        myHotels.map((hotel) => (
                            <div className="card-container" key={hotel.hotel_id}>
                                <img
                                    src="https://img.freepik.com/free-photo/beautiful-luxury-outdoor-swimming-pool-hotel-resort_74190-7433.jpg"
                                    alt="Card"
                                    className="card-img"
                                />
                                <h3 className="card-title">{hotel.hotel.name}</h3>
                                <div className="card-description">Room Cost: {hotel.hotel.totalPrice}</div>
                                <a className="btn btn-danger card-danger-btn" onClick={() => removeMyHotel(hotel.hotel_id)}>Remove</a>
                                <a href="this should go to hotel booking link" className="card-btn">Booking</a>
                            </div>
                        ))
                    )}

                    <h2>Flight</h2>
                    <div className="cards d-flex">
                        {myFlights.length === 0 ? (
                            <p style={{ fontStyle: 'italic' }}>Add a Flight to your itinerary</p>
                        ) : (

                            myFlights.map((flight) => (
                                <div className="card-container" key={flight.flight_id}>
                                    <img
                                        src="https://petapixel.com/assets/uploads/2022/05/how-to-take-photos-out-of-an-airplane-window-featured.jpg"
                                        alt="Card"
                                        className="card-img"
                                    />
                                    <h3 className="card-title">{flight.flight.carrier}</h3>
                                    <div className="card-description">{flight.flight.departureAirport} to {flight.flight.arrivalAirport}</div>
                                    <div className="card-description">Departure: {flight.flight.departureTime}</div>
                                    <div className="card-description">Cost: ${flight.flight.totalPrice}</div>
                                    <a className="btn btn-danger card-danger-btn" onClick={() => removeMyFlight(flight.flight_id)}>Remove</a>
                                    <a href="this should go to hotel booking link" className="card-btn">Booking</a>
                                </div>
                            ))
                        )}
                    </div>

                    <h2>Restaurants</h2>
                    <div className="d-flex flex-wrap">
                        {myRestaurants.length === 0 ? (
                            <p style={{ fontStyle: 'italic' }}>Add a Restaurant to your itinerary</p>
                        ) : (
                            myRestaurants.map((rest) => (
                                <div className="card-container" key={rest.restaurant_id}>
                                    <img
                                        src="https://monicafrancis.com/wp-content/uploads/2021/12/Monica-Francis-Best-NYC-Restaurants-La-Mercerie.jpg"
                                        alt="Card"
                                        className="card-img"
                                    />
                                    <h3 className="card-title">{rest.restaurant.name}</h3>
                                    <div className="card-description">{rest.restaurant.description}</div>
                                    <a className="btn btn-danger card-danger-btn" onClick={() => removeMyRestaurant(rest.restaurant_id)}>Remove</a>
                                    <a href={rest.restaurant.booking_link} className="card-btn">Booking</a>
                                </div>
                            ))
                        )}
                    </div>
                </div>

                <div className="suggested-container col-sm-6">
                    <h1>Suggested</h1>
                    <h2 className="inline-element">Hotel</h2>
                    <button className="hotel-button inline-element">
                        <Link to={`/hotelSearch/${destination}/${startDate}/${endDate}/${itinerary_id}`}>
                            Search Hotels
                        </Link>
                    </button>
                    <div className="cards d-flex">
                        {hotels.map(hotel => (
                            <div className="card-container">
                                <img
                                    src="https://monicafrancis.com/wp-content/uploads/2021/12/Monica-Francis-Best-NYC-Restaurants-La-Mercerie.jpg"
                                    alt="Card"
                                    className="card-img"
                                />
                                <div className="d-flex">
                                    <h3 className="card-title">{hotel.name}</h3>
                                </div>
                                <div className="card-description">Total Price: {hotel.totalPrice}</div>
                                <div className="card-description">Guests: {hotel.guests}  Rooms: {hotel.rooms}</div>
                                <a className="primary-btn" onClick={() => addHotel(hotel.id)}>Add to Itinerary</a>
                                <a href="https://www.booking.com" target="_blank" className="card-btn">View </a>
                            </div>
                        ))}

                    </div>

                    <h2 className="inline-element">Flight</h2>
                    <button className="flight-button inline-element">
                        <Link to={`/flightSearch/${departureAirport}/${arrivalAirport}/${startDate}/${endDate}/${itinerary_id}`}>
                            Search Flights
                        </Link>
                    </button>
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
                                <a className="primary-btn" onClick={() => addFlight(flight.id)}>Add to Itinerary</a>
                                <a href="https://www.booking.com" target="_blank" className="card-btn">View </a>
                            </div>
                        ))}
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