import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { useState } from 'react';
import BeginItinerary from './models/BeginItinerary';
import Home from './models/Home';
import NavBar from './shared/NavBar';
import UserProfile from './models/UserProfile'
import CustomerItinerary from './models/CustomerItinerary';
import Login from './models/Login';
import Register from './models/Register';

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
          <Route path='/beginitinerary' exact element={<BeginItinerary />} />
          <Route path='/userprofile' exact element={<UserProfile />} />
          <Route path='/itinerary' exact element={<CustomerItinerary />} />
          <Route path='/register' exact element={<Register />} />
        </Routes>
      </Router>

      <Login isLoginVisible={isLoginVisible} closeLogin={closeLogin} />
    </div>
  );
}

export default App;
