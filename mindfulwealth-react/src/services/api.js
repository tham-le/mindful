import axios from 'axios';
import authService from './auth';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create an axios instance with a timeout
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 5000, // 5 seconds timeout
});

// Add a request interceptor to include the auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = authService.getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add a response interceptor to handle errors
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.log('API Error:', error.message);
    
    // If unauthorized and not a login/register request, redirect to login
    if (error.response?.status === 401 && 
        !error.config.url.includes('/auth/login') && 
        !error.config.url.includes('/auth/register')) {
      authService.logout();
    }
    
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
    console.log('API sendMessage called with:', { message, contextData, conversationHistory });
    return apiClient.post('/chat', { 
      message, 
      contextData,
      conversationHistory 
    }).then(response => {
      console.log('API sendMessage response:', response);
      
      // Validate the response
      if (!response.data || !response.data.response) {
        console.error('Invalid API response format:', response);
        return { 
          data: { 
            response: "Désolé, je n'ai pas pu générer une réponse. Veuillez réessayer.", 
            financial_data: null 
          } 
        };
      }
      
      return response;
    }).catch(error => {
      console.error('Error sending message:', error.message);
      // Return mock response in development or a fallback in production
      if (process.env.NODE_ENV === 'development') {
        console.log('Returning mock response in development');
        return { data: { response: 'This is a mock response since the API is not available.', financial_data: null } };
      } else {
        return { 
          data: { 
            response: "Je rencontre des difficultés pour me connecter au serveur. Veuillez vérifier votre connexion et réessayer.", 
            financial_data: null 
          } 
        };
      }
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
  },
  
  // Dashboard endpoints
  getDashboard: () => {
    return apiClient.get('/dashboard').catch(error => {
      console.log('Error getting dashboard data:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { 
          data: {
            summary: {
              total_spent: 5240.00,
              total_budget: 8000.00,
              budget_remaining: 2760.00,
              budget_remaining_pct: 34.5,
              spending_change_pct: -0.5,
              total_saved: 1200.00,
              total_balance: 24563.00,
              monthly_income: 8350.00,
              monthly_expenses: 5240.00,
              savingsRate: 37.2,
              savingsRate_change_pct: 3.1,
              potential_growth_1yr: 1296.00,
              potential_growth_5yr: 1762.00
            },
            portfolio: {
              total: 24563.00,
              allocation: {
                stocks: 45,
                bonds: 30,
                cash: 25
              }
            },
            activity: [
              {
                id: 1,
                title: 'Salary Deposit',
                time: 'Today, 10:30 AM',
                amount: 3500.00,
                type: 'deposit'
              },
              {
                id: 2,
                title: 'Rent Payment',
                time: 'Yesterday, 2:15 PM',
                amount: 1200.00,
                type: 'withdrawal'
              },
              {
                id: 3,
                title: 'Investment Return',
                time: 'Mar 15, 9:45 AM',
                amount: 450.00,
                type: 'deposit'
              },
              {
                id: 4,
                title: 'Grocery Shopping',
                time: 'Mar 14, 6:30 PM',
                amount: 85.75,
                type: 'withdrawal'
              }
            ],
            goals: [
              {
                name: 'Emergency Fund',
                current: 7500,
                target: 10000,
                progress: 75
              },
              {
                name: 'Vacation Savings',
                current: 1350,
                target: 3000,
                progress: 45
              },
              {
                name: 'Home Down Payment',
                current: 15000,
                target: 50000,
                progress: 30
              }
            ],
            insights: [
              {
                type: 'positive',
                title: 'Positive Trend',
                description: 'Your savings rate has increased by 3.1% compared to last month. Keep up the good work!'
              },
              {
                type: 'suggestion',
                title: 'Suggestion',
                description: 'Consider increasing your retirement contributions to maximize tax benefits.'
              },
              {
                type: 'opportunity',
                title: 'Opportunity',
                description: 'Based on your spending patterns, you could save an additional €250 monthly by optimizing subscriptions.'
              }
            ]
          }
        };
      }
      throw error;
    });
  },
  
  getFinancialGoals: () => {
    return apiClient.get('/goals').catch(error => {
      console.log('Error getting financial goals:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { 
          data: [
            {
              name: 'Emergency Fund',
              current: 7500,
              target: 10000,
              progress: 75
            },
            {
              name: 'Vacation Savings',
              current: 1350,
              target: 3000,
              progress: 45
            },
            {
              name: 'Home Down Payment',
              current: 15000,
              target: 50000,
              progress: 30
            }
          ]
        };
      }
      throw error;
    });
  },
  
  getPortfolioOverview: () => {
    return apiClient.get('/portfolio').catch(error => {
      console.log('Error getting portfolio overview:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { 
          data: {
            total: 24563.00,
            allocation: {
              stocks: 45,
              bonds: 30,
              cash: 25
            },
            performance: {
              ytd: 5.2,
              oneYear: 8.7,
              threeYears: 24.3
            }
          }
        };
      }
      throw error;
    });
  },
  
  getRecentActivity: () => {
    return apiClient.get('/activity').catch(error => {
      console.log('Error getting recent activity:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { 
          data: [
            {
              id: 1,
              title: 'Salary Deposit',
              time: 'Today, 10:30 AM',
              amount: 3500.00,
              type: 'deposit'
            },
            {
              id: 2,
              title: 'Rent Payment',
              time: 'Yesterday, 2:15 PM',
              amount: 1200.00,
              type: 'withdrawal'
            },
            {
              id: 3,
              title: 'Investment Return',
              time: 'Mar 15, 9:45 AM',
              amount: 450.00,
              type: 'deposit'
            },
            {
              id: 4,
              title: 'Grocery Shopping',
              time: 'Mar 14, 6:30 PM',
              amount: 85.75,
              type: 'withdrawal'
            }
          ]
        };
      }
      throw error;
    });
  },
  
  getFinancialInsights: () => {
    return apiClient.get('/insights').catch(error => {
      console.log('Error getting financial insights:', error.message);
      // Return mock response in development
      if (process.env.NODE_ENV === 'development') {
        return { 
          data: [
            {
              type: 'positive',
              title: 'Positive Trend',
              description: 'Your savings rate has increased by 3.1% compared to last month. Keep up the good work!'
            },
            {
              type: 'suggestion',
              title: 'Suggestion',
              description: 'Consider increasing your retirement contributions to maximize tax benefits.'
            },
            {
              type: 'opportunity',
              title: 'Opportunity',
              description: 'Based on your spending patterns, you could save an additional €250 monthly by optimizing subscriptions.'
            }
          ]
        };
      }
      throw error;
    });
  }
};

export default api; 