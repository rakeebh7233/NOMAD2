import React from 'react';

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
                        <b>$ {data.price}</b>
                      </span>
                    </div>
                    <div>
                      <b>
                        {data.from.short} {'>>'} {data.to.short}
                      </b>
                    </div>
                    <div>Departure Aiport: {data.departureAirport}</div>
                    <div>Arrival Airport: {data.arrivalAirport}</div>
                    <div>Depart: {data.departureTime}</div>
                    <div>Arrive: {data.arrivalTime}</div>
                    <div>Class: {data.cabinClass}</div>
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
                    <button type="button" className="btn btn-sm btn-info">
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