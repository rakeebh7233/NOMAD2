
import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../../AuthContext';
import '../../styles/BarChart.css';

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

    const[period, setPeriod] = useState('');
    const[start_date, setStartDate] = useState('');
    const [data, setData] = useState(undefined);
    const [loading, setLoading] = useState(false);

    const { user } = useContext(AuthContext);

    useEffect(() => {
        if (user && user.email_address) { 
            const email = user.email_address;
            // console.log(email);
    
            const fetchData = async () => {
                setLoading(true);
                const period_response = await axios.get(`http://localhost:8000/savings/period/${email}`);
            
                setPeriod(period_response.data);
                console.log(period_response.data);
    
                const start_date_response = await axios.get(`http://localhost:8000/savings/start_date/${email}`);
                setStartDate(start_date_response.data);
                console.log(start_date_response.data);
    
                // const data_response = await axios.get(`http://localhost:8000/transactions/${period_response.data}/${email}/${start_date_response.data}`);
                // console.log(data_response.data)
                // const chartData = {
                //     labels: data_response.data.map(item => item.transaction_date),
                //     datasets: [
                //         {
                //             label: 'Savings Breakdown by Period',
                //             data: data_response.data.map(item => item.transaction_amount),
                //             backgroundColor: 'rgba(75, 192, 192, 0.2)',
                //             borderColor: 'rgba(75, 192, 192, 1)', 
                //             borderWidth: 1,
                //         },
                //     ],
                // };

                const groupData = (data, period) => {
                    return data.reduce((acc, item) => {
                        const date = new Date(item.transaction_date);
                        const key = period === 'monthly' 
                            ? `${date.getFullYear()}-${('0' + (date.getMonth() + 1)).slice(-2)}` // YYYY-MM
                            : `${date.getFullYear()}-W${('0' + (Math.floor(date.getDate() / 7) + 1)).slice(-2)}`; // YYYY-WW
                        acc[key] = (acc[key] || 0) + item.transaction_amount;
                        return acc;
                    }, {});
                };
                
                const data_response = await axios.get(`http://localhost:8000/transactions/${period_response.data}/${email}/${start_date_response.data}`);
                console.log(data_response.data)
                
                const groupedData = groupData(data_response.data, period_response.data);
                
                const chartData = {
                    labels: Object.keys(groupedData),
                    datasets: [
                        {
                            label: 'Savings Breakdown by ' + (period_response.data === 'monthly' ? 'Month' : 'Week'),
                            data: Object.values(groupedData),
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)', 
                            borderWidth: 1,
                        },
                    ],
                };
                // console.log(chartData);
                setData(chartData);
                // setLoading(false);
            };
    
            fetchData();
        }
    }, [user]); 

    useEffect(() => {
        if (data !== undefined) {
          setLoading(false);
          // console.log(data);
        }
    }, [data]);

    if (loading) {
        return <div>Loading...</div>;
    }
      
    return(
        <TitleCard title={"Goal Tracker"} topMargin="mt-2">
          {data && <Bar className="bar-chart" options={options} data={data} />}
        </TitleCard>
      )

}

export default BarChart;