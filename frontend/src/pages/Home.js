import React from "react";
import Select from 'react-select';
import axios from "axios";
import "../styles/Home.css";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function Home() {

  const [location, setLocation] = useState("");

  const handleSubmit = async(e) => {

    console.log("here");
    const options = {
      method: 'GET',
      url: 'http://127.0.0.1:8000/tripadvisor',
    };

    try {
      const response = await axios.request(options);
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <section>
      <div className='home-container' >
        <div class="row">
          <div class="col-lg-6 vh-100">
            <h1>YOUR NEXT JOURNEY AWAITS</h1>
            <p>We've Been Waiting for you Fellow Nomad</p>

  
              <div className='search-container'>
                <label >Where are you  off to Next?</label>
                <input id='location' type='text' placeholder='Search your location' onChange={e => setLocation(e.target.value)}/>
              </div>
              <div className='row-container'>

                <div className='search-container'>
                  <label>Check in</label>
                  <input id='check-in' type='date' />
                </div>
                <div className='search-container'>
                  <label>Check out</label>
                  <input id='check-out' type='date' />
                </div>

              </div>
              <div className='search-container'>
                <button

                  onClick = {handleSubmit}
                >
                  Explore
                </button>
              </div>

          </div>
          <div class="col-lg-6 vh-100" id="homeBackground"></div>
        </div>
      </div>
    </section>


  );
}

export default Home


