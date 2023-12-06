
import React, { useEffect, useState } from 'react';
import axios from 'axios';

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import TitleCard from '../../components/cards/TitleCard';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);


function BarChart(){

    const options = {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          }
        },
      };


    
    const email = localStorage.getItem('user').email_address;
      
      const period = axios.get(`http://localhost:8000/savings/period/${email}`);
      const start_date = axios.get(`http://localhost:8000/savings/start_date/${email}`);
      
      const [data, setData] = useState({});
      
    const fetchData = async () => {
        let response;
        if (period === 'weekly') {
            response = await axios.get(`http://localhost:8000/transactions/weekly/${email}/${start_date}`);
        } else if (period === 'monthly') {
            response = await axios.get(`http://localhost:8000/transactions/monthly/${email}/${start_date}`);
        } else if (period === 'yearly') {
            response = await axios.get(`http://localhost:8000/transactions/yearly/${email}/${start_date}`);
        }
        
        const chartData = {
            labels: response.data.map(item => item.transaction_date),
            datasets: [
                {
                    label: 'Amount',
                    data: response.data.map(item => item.transaction_amount),
                },
            ],
        };
        setData(chartData);

    };

    fetchData();

    return(
      <TitleCard title={"Goal Tracker"}>
            <Bar options={options} data={data} />
      </TitleCard>

    )

}

// const BarChart = ({ email }) => {
    
//     const period = axios.get(`http://localhost:8000/savings/period/${email}`);
//     const start_date = axios.get(`http://localhost:8000/savings/start_date/${email}`);

//     const [data, setData] = useState({});

//     useEffect(() => {
//         const fetchData = async () => {
//             let response;
//             if (period === 'weekly') {
//                 response = await axios.get(`http://localhost:8000/transactions/weekly/${email}/${start_date}`);
//             } else if (period === 'monthly') {
//                 response = await axios.get(`http://localhost:8000/transactions/monthly/${email}/${start_date}`);
//             } else if (period === 'yearly') {
//                 response = await axios.get(`http://localhost:8000/transactions/yearly/${email}/${start_date}`);
//             }

//             const chartData = {
//                 labels: response.data.map(item => item.transaction_date),
//                 datasets: [
//                     {
//                         label: 'Amount',
//                         data: response.data.map(item => item.transaction_amount),
//                     },
//                 ],
//             };

//             setData(chartData);
//         };

//         fetchData();
//     }, [period, start_date, email]);

//     return <Bar data={data} />;
// };

export default BarChart;
