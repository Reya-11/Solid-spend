import axios from 'axios';

// Create a pre-configured instance of axios
const api = axios.create({
  // The base URL for all API requests
  baseURL: 'http://127.0.0.1:8000', 
  
  // Default headers
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;