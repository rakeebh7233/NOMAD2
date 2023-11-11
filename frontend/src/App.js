import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { useState } from 'react';
import BeginItinerary from './pages/BeginItinerary';
import Home from './pages/Home';
import NavBar from './shared/NavBar';
import Form from './pages/UserProfileForm/Form';
import CustomerItinerary from './pages/CustomerItinerary';
import Login from './pages/Login';
import Register from './pages/Register';

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
          <Route path='/userprofile' exact element={<Form />} />
          <Route path='/itinerary' exact element={<CustomerItinerary />} />
          <Route path='/register' exact element={<Register />} />
        </Routes>
      </Router>

      <Login isLoginVisible={isLoginVisible} closeLogin={closeLogin} />
    </div>
  );
}

export default App;
