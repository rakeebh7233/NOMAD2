import React, { useEffect, useContext } from 'react';
import Dashboard from './Finance/Dashboard';
import '../styles/Search.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../AuthContext';

function FinanceDashboard() {
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);

  const checkUserFinance = async () => {
    if (user && user.email_address) {
      const email = user.email_address;
      try {
        const response = await axios.get(`http://localhost:8000/savings/${user.email_address}`);
        navigate("/dashboard");
        // Handle other status codes here...
      } catch (error) {
        if (error.response && error.response.status === 404) {
          navigate("/userprofile");
        }
      }

    }
  }

  useEffect(() => {
    console.log(user)
    checkUserFinance();
  }, [user]);

  return (
    <div>
    </div>
  );
}

export default FinanceDashboard;