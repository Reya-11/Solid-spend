import React, { useState, useEffect } from 'react';
import api from '../services/api';
import AddExpenseForm from '../components/AddExpenseForm';

function DashboardPage() {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchExpenses = async () => {
      try {
        const response = await api.get('/expenses/');
        setExpenses(response.data);
      } catch (err) {
        setError('Failed to fetch expenses. Is the backend server running?');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchExpenses();
  }, []); // The empty array means this effect runs once on mount

  // This function will be passed to the form component
  const handleExpenseAdded = (newExpense) => {
    // Add the new expense to the top of the list for immediate feedback
    setExpenses(prevExpenses => [newExpense, ...prevExpenses]);
  };

  // Add this function to handle the export
  const handleExport = async () => {
    try {
      const response = await api.get('/export/csv', {
        responseType: 'blob', // Important: expect a binary file response
      });

      // Create a URL for the blob
      const url = window.URL.createObjectURL(new Blob([response.data]));
      
      // Create a temporary link to trigger the download
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'expenses.csv'); // File name
      document.body.appendChild(link);
      link.click();

      // Clean up
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);

    } catch (err) {
      console.error('Failed to export CSV', err);
      // You could set an error state here to notify the user
    }
  };

  if (loading) {
    return <div className="text-center mt-8">Loading expenses...</div>;
  }

  if (error) {
    return <div className="text-center mt-8 text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Expense Dashboard</h1>
        {/* Add the export button here */}
        <button
          onClick={handleExport}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        >
          Export to CSV
        </button>
      </div>
      
      <AddExpenseForm onExpenseAdded={handleExpenseAdded} />

      <div className="space-y-4">
        {expenses.length > 0 ? (
          expenses.map((expense) => (
            <div key={expense.id} className="p-4 border rounded-lg shadow-sm bg-white">
              <div className="flex justify-between items-center">
                <span className="font-semibold">{expense.merchant}</span>
                <span className="font-bold text-lg">
                  {expense.amount} {expense.currency}
                </span>
              </div>
              <div className="text-sm text-gray-600 mt-1">
                <span>{new Date(expense.date).toLocaleDateString()}</span> | <span>{expense.category}</span>
              </div>
            </div>
          ))
        ) : (
          <p>No expenses found. Add one to get started!</p>
        )}
      </div>
    </div>
  );
}

export default DashboardPage;