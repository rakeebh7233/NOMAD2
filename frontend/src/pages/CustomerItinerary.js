import React from "react";
import Select from 'react-select';
import axios from "axios";
import "../styles/CustomItin.css";
import { useEffect, useState } from "react"; 
import { useParams } from "react-router-dom";

function CustomerItinerary(){

    const[hotelNames, sethotelyNames] = useState([]);
    const[hotelAddresses, setHotelAddresses] = useState([]);

    const[airlines, setairlines] = useState([]);
    const[airports, setairports] = useState([]);

    const[activities, setAcitivities] = useState([]);
    const [daysforActivities, setDaysForActivities] = useState([]);

    const[plannedHotelInfo, setPlannedHotelInfo] = useState([]);
    const [plannedActivitiesInfo, setPlannedActivitiesInfo] = useState([]);
    const [plannedFlightInfo, setPlanneFlightInfo] = useState([]);

    const getSuggestions = () => {
        //make calls to suggestions
    };

    const setPlannedSection = () => {
        //setThingsAsNeeded
    }




    return(
        <section id="customItinPage">
        <div className="row">

        <div className="col-sm-6">
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
        </div>

        <div className="col-sm-6">
        <h1>Suggested</h1>
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
        </div>
        </div>
       


        </section>
    );
}

export default CustomerItinerary