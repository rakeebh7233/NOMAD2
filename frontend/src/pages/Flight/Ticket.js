import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const handleBookClick = async (flight_id) => {
  try {
    // Make axios GET call here
    // const response = await axios.get(`http://localhost:8000/flight_booking/`);
    const newBooking = await axios.get(`http://localhost:8000/flight_booking/create/${flight_id}`);
    // Navigate to another page
    // const navigate = useNavigate();
    // navigate('/itineraries');
  } catch (error) {
    console.error('Error:', error);
  }
};


function Ticket(props) {
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
                    <div>Departure Aiport: {data.departureAirport}</div>
                    <div>Arrival Airport: {data.arrivalAirport}</div>
                    <div>Depart: {data.departureTime}</div>
                    <div>Arrive: {data.arrivalTime}</div>
                    <div>Class: {data.cabinClass}</div>
                    <div>Carrier: {data.carrier}</div>
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

export default Ticket;