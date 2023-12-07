import React from 'react';
import { Line } from 'react-chartjs-2';
import TitleCard from '../../components/cards/TitleCard';
import axios from 'axios';
import { useEffect, useState, useContext } from 'react';
import { AuthContext } from '../../AuthContext';

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Filler,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Filler,
    Legend
);

function LineChart() {

    const options = {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
        },
    };

    const [data, setData] = useState(undefined);
    const [loading, setLoading] = useState(false);
    
    const { user } = useContext(AuthContext);

    useEffect(() => {
        if (user && user.email_address) {
            const email = user.email_address;
            // console.log(email);

            const fetchData = async () => {
                setLoading(true);
                const daily_response = await axios.get(`http://localhost:8000/transactions/daily/${email}`);
                // console.log(daily_response.data);
                const chartData = {
                    labels: daily_response.data.map(item => item.transaction_date),
                    datasets: [
                        {
                            label: 'Savings Added',
                            data: daily_response.data.map(item => item.transaction_amount),
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

    return (
        <TitleCard title="Cumulative Savings Tracker">
            {data && <Line data={data} options={options} />}
        </TitleCard>
    );


}

export default LineChart;
