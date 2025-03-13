import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create an axios instance with a timeout
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 5000, // 5 seconds timeout
});

// Add a response interceptor to handle errors
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.log('API Error:', error.message);
    // Return a resolved promise with mock data for development
    if (process.env.NODE_ENV === 'development') {
      return Promise.resolve({
        data: { success: true, message: 'Mock response in development mode' }
      });
    }
    return Promise.reject(error);
  }
);

const api = {
  // Chat endpoints
  sendMessage: (message, contextData = null, conversationHistory = []) => {
    return apiClient.post('/chat', { 
      message, 
      contextData,
      conversationHistory 
    }).catch(error => {
      console.log('Error sending message:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { data: { response: 'This is a mock response since the API is not available.', financial_data: null } };
      }
      throw error;
    });
  },
  
  // Personality mode
  setPersonalityMode: (mode) => {
    return apiClient.post('/personality', { mode }).catch(error => {
      console.log('Error setting personality mode:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { data: { success: true } };
      }
      throw error;
    });
  },
  
  // Currency settings
  getCurrency: () => {
    return apiClient.get('/currency').catch(error => {
      console.log('Error getting currency:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { data: { currency: 'EUR' } };
      }
      throw error;
    });
  },
  
  setCurrency: (currency) => {
    return apiClient.post('/currency', { currency }).catch(error => {
      console.log('Error setting currency:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { data: { success: true } };
      }
      throw error;
    });
  },
  
  // Transaction endpoints
  getTransactions: () => {
    return apiClient.get('/transactions').catch(error => {
      console.log('Error getting transactions:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { data: [] };
      }
      throw error;
    });
  },
  
  addTransaction: (transaction) => {
    return apiClient.post('/transactions', transaction).catch(error => {
      console.log('Error adding transaction:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { data: { success: true, id: 'mock-id-' + Date.now() } };
      }
      throw error;
    });
  },
  
  // Budget endpoints
  getBudget: () => {
    return apiClient.get('/budget').catch(error => {
      console.log('Error getting budget:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { data: { total: 1000, spent: 500, categories: [] } };
      }
      throw error;
    });
  },
  
  // Saved impulses endpoints
  getSavedImpulses: () => {
    return apiClient.get('/saved-impulses').catch(error => {
      console.log('Error getting saved impulses:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { data: [] };
      }
      throw error;
    });
  },
  
  addSavedImpulse: (impulse) => {
    return apiClient.post('/saved-impulses', impulse).catch(error => {
      console.log('Error adding saved impulse:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { data: { success: true, id: 'mock-id-' + Date.now() } };
      }
      throw error;
    });
  }
};

export default api; 