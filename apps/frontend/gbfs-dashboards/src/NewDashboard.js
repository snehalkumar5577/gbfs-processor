import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import Select from 'react-select';
import 'react-datepicker/dist/react-datepicker.css';

const NewDashboard = () => {
  // Set default time range to the last 12 hours
  const now = new Date();
  const twelveHoursAgo = new Date(now.getTime() - 12 * 60 * 60 * 1000);

  const [chartData, setChartData] = useState({
    labels: [],
    datasets: []
  });

  const [startDate, setStartDate] = useState(twelveHoursAgo);
  const [endDate, setEndDate] = useState(now);
  const [providers, setProviders] = useState([]);
  const [selectedProviders, setSelectedProviders] = useState([]);

  useEffect(() => {
    const fetchProviders = async () => {
      try {
        const response = await axios.get('/api/providers');
        setProviders(response.data.map(provider => ({ value: provider, label: provider })));
      } catch (error) {
        console.error('Error fetching providers:', error);
      }
    };

    fetchProviders();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const datasets = [];
        let labelsSet = false;

        for (const provider of selectedProviders) {
          const response = await axios.get('/api/stations/timeseries', {
            params: {
              provider: provider.value,
              start_date: startDate.toISOString(),
              end_date: endDate.toISOString()
            }
          });

          const data = response.data;
          console.log(`Fetched data for ${provider.label}:`, data);

          if (Array.isArray(data)) {
            const labels = data.map(item => new Date(item.timestamp).toLocaleString());
            const values = data.map(item => item.available_bikes);

            datasets.push({
              label: `Available Bikes - ${provider.label}`,
              data: values,
              borderColor: getRandomColor(),
              borderWidth: 2,
              fill: false
            });

            // Ensure labels are set only once
            if (!labelsSet) {
              setChartData(prevState => ({
                ...prevState,
                labels: labels
              }));
              labelsSet = true;
            }
          } else {
            console.error(`Data for ${provider.label} is not an array:`, data);
          }
        }

        setChartData(prevState => ({
          ...prevState,
          datasets: datasets
        }));

        console.log('Chart data after setting state:', chartData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    if (selectedProviders.length > 0) {
      fetchData();
    }
  }, [startDate, endDate, selectedProviders]);

  const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  };

  const handleProviderChange = (selectedOptions) => {
    setSelectedProviders(selectedOptions);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>Bikes Availability</h2>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '20px' }}>
        <div style={{ marginBottom: '10px' }}>
          <label style={{ marginRight: '10px', fontWeight: 'bold' }}>Start Date: </label>
          <DatePicker selected={startDate} onChange={date => setStartDate(date)} showTimeSelect dateFormat="Pp" />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label style={{ marginRight: '10px', fontWeight: 'bold' }}>End Date: </label>
          <DatePicker selected={endDate} onChange={date => setEndDate(date)} showTimeSelect dateFormat="Pp" />
        </div>
        <div style={{ width: '100%', maxWidth: '400px' }}>
          <label style={{ marginRight: '10px', fontWeight: 'bold' }}>Select Providers: </label>
          <Select
            isMulti
            value={selectedProviders}
            onChange={handleProviderChange}
            options={providers}
          />
        </div>
      </div>
      <div style={{ marginTop: '20px' }}>
        <Line data={chartData} />
      </div>
    </div>
  );
};

export default NewDashboard;