import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export default {
  // Chat endpoints
  sendMessage(message, contextData = null, conversationHistory = []) {
    return axios.post(`${API_URL}/chat`, { 
      message, 
      contextData,
      conversationHistory 
    });
  },
  
  // Personality mode
  setPersonalityMode(mode) {
    return axios.post(`${API_URL}/personality`, { mode });
  },
  
  // Currency settings
  getCurrency() {
    return axios.get(`${API_URL}/currency`);
  },
  
  setCurrency(currency) {
    return axios.post(`${API_URL}/currency`, { currency });
  },
  
  // Transaction endpoints
  getTransactions() {
    return axios.get(`${API_URL}/transactions`);
  },
  
  addTransaction(transaction) {
    return axios.post(`${API_URL}/transactions`, transaction);
  },
  
  // Budget endpoints
  getBudget() {
    return axios.get(`${API_URL}/budget`);
  },
  
  // Saved impulses endpoints
  getSavedImpulses() {
    return axios.get(`${API_URL}/saved-impulses`);
  },
  
  addSavedImpulse(impulse) {
    return axios.post(`${API_URL}/saved-impulses`, impulse);
  }
}; 