import React from 'react';
import axios from 'axios';
// import { useNavigate } from 'react-router-dom';


const handleBookClick = async (hotel_id) => {
  try {
    // Make axios GET call here
    // const response = await axios.get(`http://localhost:8000/flight_booking/`);
    const newBooking = await axios.get(`http://localhost:8000/hotel_booking/create/${hotel_id}`);
    // Navigate to another page
    // const navigate = useNavigate();
    // navigate('/itineraries');
  } catch (error) {
    console.error('Error:', error);
  }
};


function HotelTicket(props) {
  const { filteredData} = props;

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
                  <div style={{ height: '100px', width: '140px' }}>
                    <img
                      src={data.flightImg}
                      alt="flight_img"
                      style={{ height: '100%', width: '100%' }}
                    />
                  </div>
                  <div>
                    <button type="button" className="btn btn-sm btn-info" onClick={handleBookClick(data.id)}>
                      <b>Book</b>
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