
import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../../AuthContext';
import axios from 'axios';

import Stats from './Stats';
import BarChart from './BarChart';
import LineChart from './LineChart';
import UpdateProgress from './UpdateProgress';

import CircleStackIcon  from '@heroicons/react/24/outline/CircleStackIcon'
import CreditCardIcon  from '@heroicons/react/24/outline/CreditCardIcon'
import CurrencyDollarIcon  from '@heroicons/react/24/outline/CurrencyDollarIcon'


function Dashboard() {

  const [currentSavings, setCurrentSavings] = useState(0);
  const [savingsGoal, setSavingsGoal] = useState(1000);
  const [periodGoal, setPeriodGoal] = useState(0);
  const [periodProgress, setPeriodProgress] = useState(0);


  const { user } = useContext(AuthContext);
  const email = user.email_address;
  //console.log(user.email_address);
  

  // const fetchData = async () => {
  //   const response = await axios.get(`http://localhost:8000/savings/reset_progress/${email}`);
  //   setPeriodProgress(response.data.progress_per_period);
  //   const current_progress = await axios.get(`http://localhost:8000/savings/update_progress/${email}/${0}`);
  //   setCurrentSavings(current_progress.data.current_budget);
  //   setSavingsGoal(current_progress.data.goal);
  //   setPeriodGoal(current_progress.data.goal_per_period);
  // };

  // fetchData();

  useEffect(() => {
    const response = axios.get(`http://localhost:8000/savings/reset_progress/${email}`).then(response => {
      setCurrentSavings(response.data.current_savings);
      setSavingsGoal(response.data.savings_goal);
      setPeriodGoal(response.data.period_goal);
      setPeriodProgress(response.data.progress_per_period);
      console.log(email)
    });
  }, []);

  const statsData = [
    {title:"Current Savings", value:currentSavings, icon:CurrencyDollarIcon, color:"bg-green-500"},
    {title:"Savings Goal", value:savingsGoal, icon:CircleStackIcon, color:"bg-yellow-500"},
    {title:"Period Goal", value:periodGoal, icon:CreditCardIcon, color:"bg-blue-500"},
    {title:"Period Progress", value:periodProgress, icon:CreditCardIcon, color:"bg-blue-500"},
  ]

  // return (
  //   <>
  //    {/** Savings Stats */}
  //    <div className="grid lg:grid-cols-4 mt-2 md:grid-cols-2 grid-cols-1 gap-6">
  //         {
  //             statsData.map((d, k) => {
  //                 return (
  //                     <Stats key={k} {...d} colorIndex={k}/>
  //                 )
  //             })
  //         }
  //     </div>

  //     {/** Savings Tracker Charts */}
  //     <div className="grid lg:grid-cols-2 mt-4 grid-cols-1 gap-6">
  //         <LineChart />
  //         <BarChart />
  //     </div>

  //     {/** Progress Update */}
  //     <div className="grid lg:grid-cols-2 mt-4 grid-cols-1 gap-6">
  //         <UpdateProgress />
  //     </div>
  //   </>
  // )
  return (
    <>${email}</>
  )

}





// const Savings = ({ email }) => {
//   const [currentSavings, setCurrentSavings] = useState(0);
//   const [savingsGoal, setSavingsGoal] = useState(1000);
//   const [periodGoal, setPeriodGoal] = useState(0);
//   const [periodProgress, setPeriodProgress] = useState(0);
//   const [addToSavings, setAddToSavings] = useState(0);

//   useEffect(() => {
//     const fetchData = async () => {
//       const response = await axios.get(`http://localhost:8000/savings/reset_progress/${email}`);
//       setCurrentSavings(response.data.current_savings);
//       setSavingsGoal(response.data.savings_goal);
//       setPeriodGoal(response.data.period_goal);
//       setPeriodProgress(response.data.progress_per_period);
//     };

//     fetchData();
//   }, [email]);

//   const handleAddToSavings = (e) => {
//     // Update current savings in the backend
//     axios.get(`http://localhost:8000/savings/update_progress/${email}/${addToSavings}`)
//       .then(response => {
//         e.preventDefault();
//         setCurrentSavings(response.data.current_savings);
//         setPeriodProgress(response.data.progress_per_period);
//         setAddToSavings(0);
//       })
//       .catch(error => {
//         console.error('Error fetching current savings:', error);
//       });
//   };


// };

export default Dashboard;

