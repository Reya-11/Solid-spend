import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function AnalyticsPage() {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await api.get('/analytics/');
        setAnalyticsData(response.data);
      } catch (err) {
        setError('Failed to fetch analytics data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return <div className="text-center mt-8">Loading analytics...</div>;
  }

  if (error) {
    return <div className="text-center mt-8 text-red-500">{error}</div>;
  }

  // Format date for the time series chart
  const formattedOverTimeData = analyticsData.over_time.map(item => ({
    ...item,
    date: new Date(item.date).toLocaleDateString('default', { month: 'short', year: '2-digit' }),
  }));

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Analytics Dashboard</h1>
      <p className="mb-6">All totals are normalized to your base currency: <strong>{analyticsData.base_currency}</strong></p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Spending by Category */}
        <div className="p-4 border rounded-lg bg-white shadow-md">
          <h2 className="text-xl font-semibold mb-4">Spending by Category</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analyticsData.by_category}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip formatter={(value) => new Intl.NumberFormat('en-US', { style: 'currency', currency: analyticsData.base_currency }).format(value)} />
              <Legend />
              <Bar dataKey="total" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Spending by Merchant */}
        <div className="p-4 border rounded-lg bg-white shadow-md">
          <h2 className="text-xl font-semibold mb-4">Top 20 Merchants</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analyticsData.by_merchant} layout="vertical">
              <XAxis type="number" />
              <YAxis type="category" dataKey="name" width={100} />
              <Tooltip formatter={(value) => new Intl.NumberFormat('en-US', { style: 'currency', currency: analyticsData.base_currency }).format(value)} />
              <Legend />
              <Bar dataKey="total" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Spending Over Time */}
      <div className="mt-8 p-4 border rounded-lg bg-white shadow-md">
        <h2 className="text-xl font-semibold mb-4">Spending Over Time</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={formattedOverTimeData}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip formatter={(value) => new Intl.NumberFormat('en-US', { style: 'currency', currency: analyticsData.base_currency }).format(value)} />
            <Legend />
            <Bar dataKey="total" fill="#ffc658" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default AnalyticsPage;