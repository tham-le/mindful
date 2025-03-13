import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConversationProvider } from './context/ConversationContext';
import { ThemeProvider } from './context/ThemeContext';
import { LanguageProvider } from './context/LanguageContext';
import { AuthProvider } from './context/AuthContext';
import Layout from './components/Layout';
import Login from './components/Login';
import './index.css';

// Protected route component
const ProtectedRoute = ({ children }) => {
  // Check if user is authenticated by looking for token in localStorage
  const isAuthenticated = localStorage.getItem('mindful_access_token');
  
  if (!isAuthenticated) {
    // Redirect to login if not authenticated
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

function App() {
  return (
    <Router>
      <ThemeProvider>
        <LanguageProvider>
          <AuthProvider>
            <ConversationProvider>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route 
                  path="/*" 
                  element={
                    <ProtectedRoute>
                      <Layout />
                    </ProtectedRoute>
                  } 
                />
              </Routes>
            </ConversationProvider>
          </AuthProvider>
        </LanguageProvider>
      </ThemeProvider>
    </Router>
  );
}

export default App; 