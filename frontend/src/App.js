import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { useState } from 'react';
import Home from './pages/Home';
import NavBar from './shared/NavBar';
import ProfileForm from './pages/ProfileForm';
import Itineraries from './pages/Itinerary/Itineraries';
import BeginItinerary from './pages/Itinerary/BeginItinerary';
import CustomerItinerary from './pages/CustomerItinerary';
import Login from './pages/Login';
import Register from './pages/Register';
import FlightSearch from './pages/FlightSearch';
import HotelSearch from './pages/Hotel/HotelSearch';
import FinanceDashboard from './pages/FinanceDashboard';
import { AuthProvider } from './AuthContext';

function App() {
  const [isLoginVisible, setIsLoginVisible] = useState(false);

  const handleLoginClick = () => {
    setIsLoginVisible(!isLoginVisible);
  }

  const closeLogin = () => {
    setIsLoginVisible(false);
  }

  return (
    <div>
      <NavBar handleLoginClick={handleLoginClick} />

      <Router>
        <Routes>
          <Route path='/' exact element={<Home />} />
          <Route path='/itineraries' exact element={<Itineraries />} />
          <Route path='/itineraries/:itinerary_id' exact element={<CustomerItinerary />} />
          <Route path='/itineraries/new' exact element={<BeginItinerary />} />
          <Route path='/userprofile' exact element={<ProfileForm />} />
          <Route path='/register' exact element={<Register />} />
          <Route path='/login' exact element={<Login />} />
          <Route path='/flightsearch' exact element={<FlightSearch />} />
          <Route path='/hotelsearch' exact element={<HotelSearch />} />
          <Route path='/financedashboard' exact element={<FinanceDashboard />} />
        </Routes>
      </Router>

      <Login isLoginVisible={isLoginVisible} closeLogin={closeLogin} />
    </div>
  );
}

export default App;
