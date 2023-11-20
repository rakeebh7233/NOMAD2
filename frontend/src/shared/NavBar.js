import React, { useContext } from "react";
import { AuthContext } from "../AuthContext";

function NavBar({ handleLoginClick }) {
    const {token, logout} = useContext(AuthContext);

    const handleLogout = () => {
        logout();
      };

    return (
        <nav class="navbar navbar-expand-lg">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">NOMAD</a>
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
                                    <a class="nav-link text-light" href="/itinerary">Current Itinerary</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link text-light" href="/beginitinerary">New Itinerary</a>
                                </li>
                                <li class="nav-item me-auto">
                                    <a class="nav-link text-light" href="/userprofile">User Profile</a>
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
