import React, { useContext } from "react";
import { AuthContext } from "../AuthContext";
import logo from './NOMAD_LOGO.PNG';

function NavBar({ handleLoginClick }) {
    const {token, logout} = useContext(AuthContext);

    const handleLogout = () => {
        logout();
      };

    return (
        <nav class="navbar navbar-expand-lg">
            <div class="container-fluid">
                {/* <a class="navbar-brand" href="/">NOMAD</a> */}
                <img 
                    style={{ marginRight: '10px' }}
                    src={logo} alt="logo" width="50" height="50" 
                    href="/"
                />
                <button
                    class="navbar-toggler"
                    type="button"
                    data-mdb-toggle="collapse"
                    data-mdb-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <i class="fas fa-bars"></i>
                </button>

                <div class="collapse navbar-collapse" id="navbarNav" style={{ color: '#21313c' }}>
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link active text-light" aria-current="page" href="/">Home</a>
                        </li>
                        {token && (
                            <>
                                <li class="nav-item">
                                    <a class="nav-link text-light" href="/itineraries">View Itineraries</a>
                                </li>
                                <li class="nav-item me-auto">
                                    <a class="nav-link text-light" href="/flightsearch">Flight Search</a>
                                </li>
                                <li class="nav-item me-auto">
                                    <a class="nav-link text-light" href="/hotelsearch">Hotel Search</a>
                                </li>
                                <li class="nav-item me-auto">
                                    <a class="nav-link text-light" href="/financedashboard">Finances</a>
                                </li>
                            </>
                        )}

                    </ul>
                    {token ? (
                        <button onClick={handleLogout} class="btn btn-outline-dark" type="button">
                            Sign Out
                        </button>
                    ) : (
                        <button onClick={handleLoginClick} class="btn btn-outline-dark" type="button">
                            Sign In
                        </button>
                    )}

                </div>
            </div>
        </nav>
    );
}

export default NavBar
