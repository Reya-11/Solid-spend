import React, { useState } from 'react';
import api from '../services/api';

function ReceiptUpload({ onOcrComplete }) {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/ocr/receipt', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      // Pass the parsed data up to the parent component
      onOcrComplete(response.data.parsed_data);
    } catch (err) {
      setError('Failed to process receipt. Please try again.');
      console.error(err);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="mb-4 p-4 border-dashed border-2 rounded-lg text-center">
      <label htmlFor="receipt-upload" className="cursor-pointer">
        <span className="text-blue-500 font-semibold">Upload a Receipt</span>
        <p className="text-sm text-gray-500">to auto-fill the form</p>
      </label>
      <input
        id="receipt-upload"
        type="file"
        className="hidden"
        onChange={handleFileChange}
        disabled={isUploading}
      />
      {isUploading && <p className="mt-2 text-sm">Processing receipt...</p>}
      {error && <p className="mt-2 text-red-500">{error}</p>}
    </div>
  );
}

export default ReceiptUpload;