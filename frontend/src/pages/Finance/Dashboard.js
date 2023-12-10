import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../../AuthContext';
import axios from 'axios';

import Stats from './Stats';
import BarChart from './BarChart';
import LineChart from './LineChart';
import UpdateProgress from './UpdateProgress';
import RemoveProgress from './RemoveProgress';
import '../../styles/Dashboard.css';


function Dashboard() {
  const [currentSavings, setCurrentSavings] = useState(0);
  const [savingsGoal, setSavingsGoal] = useState(1000);
  const [periodGoal, setPeriodGoal] = useState(0);
  const [periodProgress, setPeriodProgress] = useState(0);
  const [statsData, setStatsData] = useState(undefined);
  const [loading, setLoading] = useState(false);

  const { user } = useContext(AuthContext);

  // const checkUserFinance = async () => {


  useEffect(() => {
    // checkUserFinance();
    if (user && user.email_address) {
      const email = user.email_address;
      // console.log(email);

      const fetchData = async () => {
        setLoading(true);
        const email = user.email_address;
        //console.log(user.email_address);
        const response = await axios.get(`http://localhost:8000/savings/reset_progress/${email}`);
        setPeriodProgress(response.data.progress_per_period);

        const current_progress = await axios.get(`http://localhost:8000/savings/update_progress/${email}/${0}`);
        //console.log(current_progress.data);
        setCurrentSavings(current_progress.data.current_budget);
        setSavingsGoal(current_progress.data.goal);
        setPeriodGoal(current_progress.data.goal_per_period);
        const newStatsData = [
          { title: "Current Savings", value: current_progress.data.current_budget, color: "bg-green-500" },
          { title: "Savings Goal", value: current_progress.data.goal, color: "bg-yellow-500" },
          { title: "Period Goal", value: current_progress.data.goal_per_period.toFixed(2), color: "bg-blue-500" },
          { title: "Period Progress", value: current_progress.data.progress_per_period, color: "bg-blue-500" },
        ];
        // console.log(newStatsData);
        setStatsData(newStatsData);
        setLoading(false);
      };

      fetchData();
    }
  }, [user]);

  useEffect(() => {
    if (statsData !== undefined) {
      //setLoading(false);
      console.log(statsData);
    }
  }, [statsData]);

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <>
      <div className="dashboard-grid">
        <div className="grid lg:grid-cols-4 mt-2 md:grid-cols-2 grid-cols-1 gap-6 stats-container">
          {statsData !== undefined && statsData.map((stat) => (
          <Stats title={stat.title} value={stat.value} color={stat.color} className="stats-item" />
          ))}
        </div>
        <div>
          <BarChart className="chart-container"/>
        </div>
        <div>
          <LineChart className="chart-container"/>
        </div>
        <div className="update-progress-container">
          <UpdateProgress />
        </div>
        <div className="update-progress-container">
          <RemoveProgress />
        </div>
      </div>
      {/* <div className="grid lg:grid-cols-2 mt-4 grid-cols-1 gap-6">
      <BarChart />
      <LineChart />
    </div>
    <div className="grid lg:grid-cols-2 mt-4 grid-cols-1 gap-6">
      <UpdateProgress />
    </div> */}
    </>
  )

}

export default Dashboard;

