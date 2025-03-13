import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';
const AUTH_URL = `${API_URL}/auth`;

// Create an axios instance for auth requests
const authClient = axios.create({
  baseURL: AUTH_URL,
  timeout: 5000, // 5 seconds timeout
});

// Local storage keys
const TOKEN_KEY = 'mindful_access_token';
const REFRESH_TOKEN_KEY = 'mindful_refresh_token';
const USER_KEY = 'mindful_user';

// Add request interceptor to include token in requests
authClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle token refresh
authClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If error is 401 and we haven't tried to refresh the token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
        if (!refreshToken) {
          // No refresh token, logout
          authService.logout();
          return Promise.reject(error);
        }
        
        const response = await authClient.post('/refresh', {}, {
          headers: { 'Authorization': `Bearer ${refreshToken}` }
        });
        
        // Store the new access token
        const { access_token } = response.data;
        localStorage.setItem(TOKEN_KEY, access_token);
        
        // Retry the original request with the new token
        originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
        return axios(originalRequest);
      } catch (refreshError) {
        // If refresh fails, logout
        authService.logout();
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

const authService = {
  // Register a new user
  register: async (name, email, password) => {
    try {
      const response = await authClient.post('/register', {
        name,
        email,
        password
      });
      
      // Store tokens and user data
      const { access_token, refresh_token, user } = response.data;
      localStorage.setItem(TOKEN_KEY, access_token);
      localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token);
      localStorage.setItem(USER_KEY, JSON.stringify(user));
      
      return { success: true, user };
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Registration failed' 
      };
    }
  },
  
  // Login a user
  login: async (email, password) => {
    try {
      const response = await authClient.post('/login', {
        email,
        password
      });
      
      // Store tokens and user data
      const { access_token, refresh_token, user } = response.data;
      localStorage.setItem(TOKEN_KEY, access_token);
      localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token);
      localStorage.setItem(USER_KEY, JSON.stringify(user));
      
      return { success: true, user };
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Login failed' 
      };
    }
  },
  
  // Create a demo user
  createDemo: async () => {
    try {
      const response = await authClient.post('/demo');
      
      // Store tokens and user data
      const { access_token, refresh_token, user } = response.data;
      localStorage.setItem(TOKEN_KEY, access_token);
      localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token);
      localStorage.setItem(USER_KEY, JSON.stringify(user));
      
      return { success: true, user };
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Failed to create demo user' 
      };
    }
  },
  
  // Logout the current user
  logout: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    
    // Redirect to login page
    window.location.href = '/login';
  },
  
  // Get the current user
  getCurrentUser: () => {
    const userStr = localStorage.getItem(USER_KEY);
    if (!userStr) return null;
    
    try {
      return JSON.parse(userStr);
    } catch (e) {
      return null;
    }
  },
  
  // Check if user is logged in
  isLoggedIn: () => {
    return !!localStorage.getItem(TOKEN_KEY);
  },
  
  // Get the current access token
  getToken: () => {
    return localStorage.getItem(TOKEN_KEY);
  },
  
  // Update user preferences
  updatePreferences: async (preferences) => {
    try {
      const token = localStorage.getItem(TOKEN_KEY);
      if (!token) {
        return { success: false, message: 'Not authenticated' };
      }
      
      const response = await axios.put(`${API_URL}/auth/preferences`, preferences, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      // Update user data in local storage
      const updatedUser = response.data.user;
      localStorage.setItem(USER_KEY, JSON.stringify(updatedUser));
      
      return { success: true, user: updatedUser };
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Failed to update preferences' 
      };
    }
  }
};

export default authService; 