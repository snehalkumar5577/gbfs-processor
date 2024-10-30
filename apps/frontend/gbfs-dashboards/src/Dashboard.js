// src/Dashboard.js

import React, { useEffect, useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import "chart.js/auto"; // Ensures Chart.js is loaded

const Dashboard = () => {
  const [bikeData, setBikeData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch bike availability summary from the backend
    const fetchData = async () => {
      try {
        console.log("process.env.REACT_APP_BACKEND_API_URL", process.env.REACT_APP_BACKEND_API_URL);
        const response = await axios.get('/api/stations/summary');
        setBikeData(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching bike data", error);
      }
    };
    fetchData();
  }, []);

  // Prepare data for the Bar chart
  const chartData = {
    labels: bikeData.map((item) => item.provider),
    datasets: [
      {
        label: "Available Bikes",
        data: bikeData.map((item) => item.total_bikes),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
    },
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Available Bikes by Provider</h2>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default Dashboard;
