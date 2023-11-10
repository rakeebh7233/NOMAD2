import React from "react";
import Select from 'react-select';
import axios from "axios";
import "../styles/Home.css";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function Home() {
  return (
    <section>
      <div className='home-container' >
        <div class="row">
          <div class="col-lg-6 vh-100">
            <h1>YOUR NEXT JOURNEY AWAITS</h1>
            <p>We've Been Waiting for you Fellow Nomad</p>

            <form className='search'>
              <div className='search-container'>
                <label >Where are you  off to Next?</label>
                <input id='location' type='text' placeholder='Search your location' />
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
                  className='search-btn'
                  type='submit'
                //onClick={}
                >
                  Explore
                </button>
              </div>
            </form>
          </div>
          <div class="col-lg-6 vh-100" id="homeBackground"></div>
        </div>
      </div>
    </section>


  );
}

export default Home


