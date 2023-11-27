import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { useState } from 'react';
import Home from './pages/Home';
import NavBar from './shared/NavBar';
import Form from './pages/UserProfileForm/Form';
import Itineraries from './pages/Itineraries';
import BeginItinerary from './pages/BeginItinerary';
import CustomerItinerary from './pages/CustomerItinerary';
import Login from './pages/Login';
import Register from './pages/Register';
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
    <AuthProvider>
      <NavBar handleLoginClick={handleLoginClick} />

      <Router>
          <Routes>
            <Route path='/' exact element={<Home />} />
            <Route path='/itineraries' exact element={<Itineraries />} />
            <Route path='/currentitinerary' exact element={<CustomerItinerary />} />
            <Route path='/itineraries/new' exact element={<BeginItinerary />} />
            <Route path='/userprofile' exact element={<Form />} />
            <Route path='/register' exact element={<Register />} />
          </Routes>
      </Router>

      <Login isLoginVisible={isLoginVisible} closeLogin={closeLogin} />
    </AuthProvider>
  );
}

export default App;
