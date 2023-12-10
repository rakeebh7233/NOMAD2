import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';

function Ticket(props) {
  const { itinID } = useParams();
  const { filteredData } = props;
  const navigate = useNavigate();

  const addFlight = async (flight_id) => {
    const response = await fetch('http://localhost:8000/flight_booking/new_booking', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        flight_id: flight_id,
        itinerary_id: itinID
      })
    });

    if (response.ok) {
      console.log("Added flight")
      navigate("/itineraries/" + itinID)
    } else {
      throw new Error("Flight not added");
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
                        <b>$ {(data.totalPrice).toFixed(2)}</b>
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
                  <div style={{ height: '100px', width: '140px' }}></div>
                  {itinID &&
                    <div>
                      <button type="button" className="btn btn-sm btn-info" onClick={() => addFlight(data.id)}>
                        <b>Add to Itinerary</b>
                      </button>
                    </div>
                  }
                  { !itinID &&
                    <button type="button" class="btn btn-primary btn-lg">
                      <a class="nav-link text-light" href="/itineraries/new">Create New Itinerary</a>
                    </button>
                  }
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