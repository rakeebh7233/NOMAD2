import React, { useEffect, useState } from "react";
import HotelResult from "./HotelResult";
import axios from "axios";
import { useParams } from "react-router-dom";

function HotelSearch() {
  const { city, startDate, endDate, itinID } = useParams();

  const [location, setLocation] = useState(city);
  const [checkInDate, setCheckInDate] = useState(startDate);
  const [checkOutDate, setCheckOutDate] = useState(endDate);
  const [guests, setGuests] = useState(0);
  const [rooms, setRooms] = useState(0);
  const [filteredData, setFilteredData] = useState([]);

  const [isSearchClicked, setIsSearchClicked] = useState(false);

  const handleFocus = (e) => {
    e.currentTarget.type = "date";
  };
  const handleBlur = (e) => {
    e.currentTarget.type = "text";
  };

  const handleFilter = async () => {
    try {
        const response = await axios.get(`http://localhost:8000/hotel/location_internal/${location}`);
        console.log("Location DB Response: " + response.data)
        let locationId 
        if (response.data.isInDB) {
            locationId = response.data.geoId
            console.log(locationId)
        } else {
            const getlocId = await axios.get(`http://localhost:8000/hotel/location_external/${location}`);
            locationId = getlocId.data.geoId
            console.log(locationId)
        }
        console.log(locationId)
        const hotel_search = await axios.get(`http://localhost:8000/hotel/hotel_internal/${locationId}/${checkInDate}/${checkOutDate}/${guests}/${rooms}`).then((response) => {
            if (response.data.length !== 0) {
                setFilteredData(response.data);
                console.log(response.data)
            } else {
                const external_search = axios.get(`http://localhost:8000/hotel/hotel_external/${locationId}/${checkInDate}/${checkOutDate}/${guests}/${rooms}`).then((response) => {
                    if (response.data.length !== 0) {
                        setFilteredData(response.data);
                        console.log(response.data)
                    } else {
                        console.log("No hotels found")
                    }
                });
            }
        });
    } catch (error) {
        console.log(error);
    }
  };
    


  const handleSearch = async () => {
    if (!location) {
        alert("You must specify a Location (City)!");
    } else if (!checkInDate) {
        alert("You must specify a Check-In Date!");
    } else if (!checkOutDate) {
        alert("You must specify a Check-Out Date!");
    } else if (!guests) {
        alert("You must specify the number of Guests!");
    }
    else if (!rooms) {
        alert("You must specify the number of Rooms!");
    }
    if (location && checkInDate && checkOutDate && guests && rooms) {
        setIsSearchClicked(true);
        await handleFilter();
    }
  };

  return (
    <div id="hotelSearch">
      <div className="row mt-4 ml-5 mr-5">
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <div className="card">
                <div className="card-body">
                  <div className="btn-group d-flex justify-content-center">
                    Hotel Booking 
                  </div>
                  <input
                    type="text"
                    placeholder="Enter Desired Location (City)"
                    className="form-control mt-4"
                    value={city}
                    onChange={(e) => setLocation(e.target.value)}
                  />
                  <input
                    type="date"
                    placeholder="Enter Check-In Date"
                    className="form-control mt-2"
                    onFocus={handleFocus}
                    onBlur={handleBlur}
                    value={startDate}
                    onChange={(e) => setCheckInDate(e.target.value)}
                  />
                  <input
                    type="date"
                    placeholder="Enter Check-Out Date"
                    className="form-control mt-2"
                    onFocus={handleFocus}
                    onBlur={handleBlur}
                    value={endDate}
                    onChange={(e) => setCheckOutDate(e.target.value)}
                  />
                  <input
                    type="number"
                    placeholder="Enter Number of Guests"
                    className="form-control mt-2"
                    onChange={(e) => setGuests(e.target.value)}
                  />
                  <input
                    type="number"
                    placeholder="Enter Number of Rooms"
                    className="form-control mt-2"
                    onChange={(e) => setRooms(e.target.value)}
                  />
                  <div>
                    <button
                      type="button"
                      className="btn search_btn"
                      onClick={handleSearch}
                    >
                      <b>Search</b>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-8">
          <HotelResult
            filteredData={filteredData}
            isSearchClicked={isSearchClicked}
          />
        </div>
      </div>
    </div>
  );
}

export default HotelSearch;