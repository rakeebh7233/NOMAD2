
import React from 'react';
import { Line } from 'react-chartjs-2';
import TitleCard from '../../components/cards/TitleCard';
import axios from 'axios';
import { useEffect, useState } from 'react';

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

    const [data, setData] = useState({});
    const email = localStorage.getItem('user').email_address;

    const fetchData = async () => {
        let response;
        response = await axios.get(`http://localhost:8000/transactions/daily/${email}`);

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

    return (
        <TitleCard title="Cumulative Savings Tracker">
            <Line data={data} options={options} />
        </TitleCard>
    );


}







// const LineChart = ({ email }) => {

//     const [data, setData] = useState({});

//     useEffect(() => {
//         const fetchData = async () => {
//             let response;
//             response = await axios.get(`http://localhost:8000/transactions/daily/${email}`);

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
//     }, [email]);

//     return <Line data={data} />;
// };

export default LineChart;
