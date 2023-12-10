import React from "react";
import axios from "axios";
import "../styles/Home.css";
import { useContext, useState } from "react";
import { AuthContext } from "../AuthContext";
import { useNavigate } from "react-router-dom";
import logo from '../shared/NOMAD_LOGO.PNG';

function Home() {
  const { token, user } = useContext(AuthContext);
  const [location, setLocation] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const Navigate = useNavigate();

  const handleSubmit = async (e) => {
    Navigate("/flightsearch")
  };

  return (
    <section>
      <div className='home-container' >
        <div class="row">
          <div class="col-lg-6 vh-100">
            <div class=" d-flex justify-content-center align-items-center mt-5" >
              <img
                style={{ margin: "auto" }}
                src={logo} alt="logo" width="350" height="300"
                href="/"
              />
            </div>
            <h1>YOUR NEXT JOURNEY AWAITS</h1>

            {token && user && (<p>Welcome {user.firstName} {user.lastName}</p>)}
            <p>We've Been Waiting for you Fellow Nomad</p>

            <div className='search-container'>
              <div><label >Where are you  off to Next?</label></div>
              <div>
                <input id='location' type='text' placeholder='Search your location' onChange={e => setLocation(e.target.value)} />

                <div className='search-container'>
                  <label>Check in</label>
                  <input id='check-in' type='date' onChange={e => setStartDate(e.target.value)} />
                </div>
                <div className='search-container'>
                  <label>Check out</label>
                  <input id='check-out' type='date' onChange={e => setEndDate(e.target.value)} />
                </div>

                <button
                  style={{ marginLeft: "10px" }}
                  class="btn btn-primary" data-mdb-ripple-init="light"
                  onClick={handleSubmit}>
                  Explore
                </button>
              </div>
            </div>
          </div>
          <div class="col-lg-6 vh-100" id="homeBackground"></div>
        </div>
      </div>
    </section>


  );
}

export default Home


