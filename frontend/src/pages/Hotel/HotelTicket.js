import React from 'react';
import axios from 'axios';
import { useParams, useNavigate } from "react-router-dom";

function HotelTicket(props) {
  const { itinID } = useParams();
  const { filteredData } = props;
  const navigate = useNavigate();

  const addHotel = async (hotel_id) => {
    const response = await fetch('http://localhost:8000/hotel_booking/new_booking', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        hotel_id: hotel_id,
        itinerary_id: itinID
      })
    });
    if (response.ok) {
      console.log("Added hotel")
      navigate("/itineraries/"+itinID)
    } else {
      throw new Error("Hotel not added");
    }
  }

  return (
    <>
      {filteredData.map((data, i) => {
        return (
          <div className="card mb-3" id="ticket_card" key={i}>
            <div className="card-body">
              <div style={{ display: 'flex' }}>
                <div
                  style={{
                    width: '60%',
                    fontSize: '13px',
                    display: 'flex',
                    lineHeight: '1.5rem',
                  }}
                >
                  <div>
                    <div
                      style={{
                        marginBottom: '6px',
                        display: 'flex',
                        justifyContent: 'space-between',
                      }}
                    >
                      <span>
                        <b>$ {data.totalPrice}</b>
                      </span>
                    </div>
                    <div>
                      {/* <b>
                        {data.from.short} {'>>'} {data.to.short}
                      </b> */}
                    </div>
                    <div>Hotel Name: {data.name}</div>
                    <div>Location: {data.location}</div>
                    <div>Check-In Date: {data.checkInDate}</div>
                    <div>Check-Out Date: {data.checkOutDate}</div>
                    <div>Num Guests: {data.guests}</div>
                    <div>Num Rooms: {data.rooms}</div>
                    <div>Rating: {data.reviewScore}</div>
                  </div>
                </div>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    width: '40%',
                    flexDirection: 'column',
                  }}
                >
                  <div style={{ height: '70px', width: '140px' }}> 
                    {/* <img
                      src={data.flightImg}
                      alt="flight_img"
                      style={{ height: '100%', width: '100%' }}
                    />   */}
                  </div> 
                  <div>
                    <button type="button" className="btn btn-sm btn-info" onClick={() => addHotel(data.id)}>
                      <b>Add to Itinerary</b>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </>
  );
}

export default HotelTicket;