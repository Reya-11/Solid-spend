import React, { useState } from 'react';
import api from '../services/api';
import ReceiptUpload from './ReceiptUpload'; // Import the component

function AddExpenseForm({ onExpenseAdded }) {
  const [formData, setFormData] = useState({
    merchant: '',
    amount: '',
    currency: 'USD',
    category: '',
    date: new Date().toISOString().split('T')[0], // Defaults to today
  });
  const [error, setError] = useState('');

  // This function will receive data from the ReceiptUpload component
  const handleOcrData = (ocrData) => {
    setFormData(prevState => ({
      ...prevState,
      // Use the OCR data if available, otherwise keep the existing value
      merchant: ocrData.merchant || prevState.merchant,
      amount: ocrData.amount || prevState.amount,
      date: ocrData.date ? new Date(ocrData.date).toISOString().split('T')[0] : prevState.date,
    }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.merchant || !formData.amount || !formData.category) {
      setError('Please fill out all required fields.');
      return;
    }

    try {
      const response = await api.post('/expenses/', formData);
      // Call the function passed from the parent to update the list
      onExpenseAdded(response.data); 
      // Reset form
      setFormData({
        merchant: '',
        amount: '',
        currency: 'USD',
        category: '',
        date: new Date().toISOString().split('T')[0],
      });
    } catch (err) {
      setError('Failed to add expense.');
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded-lg bg-white shadow-md mb-6">
      {/* Add the upload component here */}
      <ReceiptUpload onOcrComplete={handleOcrData} />

      <h2 className="text-xl font-semibold mb-4">Add New Expense</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input type="text" name="merchant" value={formData.merchant} onChange={handleChange} placeholder="Merchant" className="p-2 border rounded" />
        <input type="number" name="amount" value={formData.amount} onChange={handleChange} placeholder="Amount" className="p-2 border rounded" />
        <input type="text" name="currency" value={formData.currency} onChange={handleChange} placeholder="Currency (e.g., USD)" className="p-2 border rounded" />
        <input type="text" name="category" value={formData.category} onChange={handleChange} placeholder="Category" className="p-2 border rounded" />
        <input type="date" name="date" value={formData.date} onChange={handleChange} className="p-2 border rounded" />
      </div>
      <button type="submit" className="mt-4 w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
        Add Expense
      </button>
    </form>
  );
}

export default AddExpenseForm;