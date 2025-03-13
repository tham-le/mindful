import React, { useState, useEffect } from 'react';
import ChatInterface from './ChatInterface';
import UserProfile from './UserProfile';
import Dashboard from './Dashboard';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';

const Layout = () => {
  const [activeTab, setActiveTab] = useState('chat');
  const { t } = useLanguage();
  const { theme, layoutStyle } = useTheme();

  // Function to handle tab changes and scroll to top
  const handleTabChange = (tab) => {
    setActiveTab(tab);
    // Scroll to top when changing tabs
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Background style based on theme and layout style
  const getBackgroundStyle = () => {
    if (layoutStyle === 'gradient') {
      return {
        backgroundImage: theme === 'dark' 
          ? 'linear-gradient(to bottom right, #1e1e52, #4a1e52, #521e3a)'
          : 'linear-gradient(to bottom right, #e0f2fe, #ddd6fe, #fae8ff)'
      };
    } else {
      // Modern style with solid colors
      return {
        backgroundColor: theme === 'dark' ? '#121212' : '#f8fafc',
        backgroundImage: theme === 'dark'
          ? 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23232323\' fill-opacity=\'0.4\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")'
          : 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23e2e8f0\' fill-opacity=\'0.4\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")'
      };
    }
  };

  // Header style based on theme and layout style
  const getHeaderStyle = () => {
    if (layoutStyle === 'gradient') {
      return { 
        backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.3)' : 'rgba(255, 255, 255, 0.7)',
        backdropFilter: 'blur(8px)',
        borderBottom: `1px solid ${theme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'}`
      };
    } else {
      return {
        backgroundColor: theme === 'dark' ? '#1e1e1e' : '#ffffff',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        borderBottom: `1px solid ${theme === 'dark' ? '#333' : '#e5e7eb'}`
      };
    }
  };

  // Navigation style based on theme and layout style
  const getNavStyle = () => {
    if (layoutStyle === 'gradient') {
      return { 
        backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.2)' : 'rgba(255, 255, 255, 0.5)',
        backdropFilter: 'blur(8px)'
      };
    } else {
      return {
        backgroundColor: theme === 'dark' ? '#1e1e1e' : '#ffffff',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        borderRight: theme === 'dark' ? '1px solid #333' : '1px solid #e5e7eb'
      };
    }
  };

  // Mobile navigation style based on theme and layout style
  const getMobileNavStyle = () => {
    if (layoutStyle === 'gradient') {
      return { 
        backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.2)' : 'rgba(255, 255, 255, 0.5)',
        backdropFilter: 'blur(8px)',
        borderTop: `1px solid ${theme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'}`
      };
    } else {
      return {
        backgroundColor: theme === 'dark' ? '#1e1e1e' : '#ffffff',
        boxShadow: '0 -1px 3px rgba(0,0,0,0.1)',
        borderTop: `1px solid ${theme === 'dark' ? '#333' : '#e5e7eb'}`
      };
    }
  };

  // Button style based on active state, theme, and layout style
  const getButtonStyle = (isActive) => {
    if (layoutStyle === 'gradient') {
      return isActive
        ? theme === 'dark' 
          ? 'bg-white/10 text-white shadow-lg shadow-primary/20'
          : 'bg-black/10 text-black shadow-lg shadow-primary/20'
        : theme === 'dark'
          ? 'text-white/70 hover:bg-white/5'
          : 'text-black/70 hover:bg-black/5';
    } else {
      return isActive
        ? theme === 'dark'
          ? 'bg-primary text-white shadow-md'
          : 'bg-primary text-white shadow-md'
        : theme === 'dark'
          ? 'text-gray-400 hover:text-white hover:bg-gray-800'
          : 'text-gray-500 hover:text-gray-900 hover:bg-gray-100';
    }
  };

  // Mobile button style based on active state, theme, and layout style
  const getMobileButtonStyle = (isActive) => {
    if (layoutStyle === 'gradient') {
      return isActive
        ? theme === 'dark' 
          ? 'bg-white/10 text-white scale-105 shadow-lg shadow-primary/20'
          : 'bg-black/10 text-black scale-105 shadow-lg shadow-primary/20'
        : theme === 'dark'
          ? 'text-white/70 hover:bg-white/5'
          : 'text-black/70 hover:bg-black/5';
    } else {
      return isActive
        ? theme === 'dark'
          ? 'text-primary font-medium'
          : 'text-primary font-medium'
        : theme === 'dark'
          ? 'text-gray-400 hover:text-white'
          : 'text-gray-500 hover:text-gray-900';
    }
  };

  return (
    <div className="min-h-screen flex flex-col" style={getBackgroundStyle()}>
      {/* Fixed header with logo */}
      <div className="fixed top-0 left-0 right-0 z-50">
        {/* App header */}
        <header className="px-4 py-3" style={getHeaderStyle()}>
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <div className="flex items-center">
              {layoutStyle === 'modern' && (
                <div className="mr-2">
                  {theme === 'dark' ? (
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="#6d28d9"/>
                      <path d="M12 17C14.7614 17 17 14.7614 17 12C17 9.23858 14.7614 7 12 7C9.23858 7 7 9.23858 7 12C7 14.7614 9.23858 17 12 17Z" fill="#6d28d9"/>
                      <path d="M12 9C13.6569 9 15 10.3431 15 12C15 13.6569 13.6569 15 12 15C10.3431 15 9 13.6569 9 12C9 10.3431 10.3431 9 12 9Z" fill="#ffffff"/>
                    </svg>
                  ) : (
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="#6d28d9"/>
                      <path d="M12 17C14.7614 17 17 14.7614 17 12C17 9.23858 14.7614 7 12 7C9.23858 7 7 9.23858 7 12C7 14.7614 9.23858 17 12 17Z" fill="#6d28d9"/>
                      <path d="M12 9C13.6569 9 15 10.3431 15 12C15 13.6569 13.6569 15 12 15C10.3431 15 9 13.6569 9 12C9 10.3431 10.3431 9 12 9Z" fill="#1e1e1e"/>
                    </svg>
                  )}
                </div>
              )}
              <div className={layoutStyle === 'gradient' 
                ? "text-transparent bg-clip-text bg-gradient-to-r from-primary to-pink-500 text-2xl font-extrabold"
                : "text-primary text-2xl font-extrabold"
              }>
                {t('appName')}
              </div>
              <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                layoutStyle === 'gradient' 
                  ? "bg-primary/20 text-primary animate-pulse"
                  : "bg-primary/10 text-primary"
              }`}>
                {t('ai')}
              </span>
            </div>
          </div>
        </header>
      </div>
      
      {/* Main content with padding for fixed header */}
      <div className="flex-1 flex flex-col md:flex-row pt-16 pb-16 md:pb-0">
        {/* Desktop sidebar navigation - fixed on the left */}
        <nav className="hidden md:flex fixed left-0 top-16 bottom-0 flex-col w-20 lg:w-64 p-4 z-40" style={getNavStyle()}>
          <div className="space-y-2">
            <button
              onClick={() => handleTabChange('profile')}
              className={`w-full p-3 lg:pl-4 rounded-xl flex items-center transition-all duration-300 ${getButtonStyle(activeTab === 'profile')}`}
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                className="h-6 w-6 lg:mr-3" 
                viewBox="0 0 20 20" 
                fill="currentColor"
              >
                <path 
                  fillRule="evenodd" 
                  d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" 
                  clipRule="evenodd" 
                />
              </svg>
              <span className="hidden lg:block">{t('profile')}</span>
            </button>
            
            <button
              onClick={() => handleTabChange('chat')}
              className={`w-full p-3 lg:pl-4 rounded-xl flex items-center transition-all duration-300 ${getButtonStyle(activeTab === 'chat')}`}
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                className="h-6 w-6 lg:mr-3" 
                viewBox="0 0 20 20" 
                fill="currentColor"
              >
                <path 
                  fillRule="evenodd" 
                  d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" 
                  clipRule="evenodd" 
                />
              </svg>
              <span className="hidden lg:block">{t('chat')}</span>
            </button>
            
            <button
              onClick={() => handleTabChange('dashboard')}
              className={`w-full p-3 lg:pl-4 rounded-xl flex items-center transition-all duration-300 ${getButtonStyle(activeTab === 'dashboard')}`}
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                className="h-6 w-6 lg:mr-3" 
                viewBox="0 0 20 20" 
                fill="currentColor"
              >
                <path 
                  d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" 
                />
                <path 
                  d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" 
                />
              </svg>
              <span className="hidden lg:block">{t('dashboard')}</span>
            </button>
          </div>
          
          <div className="mt-auto pt-6 hidden lg:block">
            {layoutStyle === 'modern' && theme === 'dark' && (
              <div className="mb-4 flex justify-center">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMkMyIDE3LjUyIDYuNDggMjIgMTIgMjJDMTcuNTIgMjIgMjIgMTcuNTIgMjIgMTJDMjIgNi40OCAxNy41MiAyIDEyIDJaTTEyIDIwQzcuNTkgMjAgNCAxNi40MSA0IDEyQzQgNy41OSA3LjU5IDQgMTIgNEMxNi40MSA0IDIwIDcuNTkgMjAgMTJDMjAgMTYuNDEgMTYuNDEgMjAgMTIgMjBaIiBmaWxsPSIjNmQyOGQ5Ii8+PHBhdGggZD0iTTEyIDE3QzE0Ljc2MTQgMTcgMTcgMTQuNzYxNCAxNyAxMkMxNyA5LjIzODU4IDE0Ljc2MTQgNyAxMiA3QzkuMjM4NTggNyA3IDkuMjM4NTggNyAxMkM3IDE0Ljc2MTQgOS4yMzg1OCAxNyAxMiAxN1oiIGZpbGw9IiM2ZDI4ZDkiLz48cGF0aCBkPSJNMTIgOUMxMy42NTY5IDkgMTUgMTAuMzQzMSAxNSAxMkMxNSAxMy42NTY5IDEzLjY1NjkgMTUgMTIgMTVDMTAuMzQzMSAxNSA5IDEzLjY1NjkgOSAxMkM5IDEwLjM0MzEgMTAuMzQzMSA5IDEyIDlaIiBmaWxsPSIjZmZmZmZmIi8+PC9zdmc+" alt="Cartoon coin" className="w-16 h-16" />
              </div>
            )}
            {layoutStyle === 'modern' && theme === 'light' && (
              <div className="mb-4 flex justify-center">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMkMyIDE3LjUyIDYuNDggMjIgMTIgMjJDMTcuNTIgMjIgMjIgMTcuNTIgMjIgMTJDMjIgNi40OCAxNy41MiAyIDEyIDJaTTEyIDIwQzcuNTkgMjAgNCAxNi40MSA0IDEyQzQgNy41OSA3LjU5IDQgMTIgNEMxNi40MSA0IDIwIDcuNTkgMjAgMTJDMjAgMTYuNDEgMTYuNDEgMjAgMTIgMjBaIiBmaWxsPSIjNmQyOGQ5Ii8+PHBhdGggZD0iTTEyIDE3QzE0Ljc2MTQgMTcgMTcgMTQuNzYxNCAxNyAxMkMxNyA5LjIzODU4IDE0Ljc2MTQgNyAxMiA3QzkuMjM4NTggNyA3IDkuMjM4NTggNyAxMkM3IDE0Ljc2MTQgOS4yMzg1OCAxNyAxMiAxN1oiIGZpbGw9IiM2ZDI4ZDkiLz48cGF0aCBkPSJNMTIgOUMxMy42NTY5IDkgMTUgMTAuMzQzMSAxNSAxMkMxNSAxMy42NTY5IDEzLjY1NjkgMTUgMTIgMTVDMTAuMzQzMSAxNSA5IDEzLjY1NjkgOSAxMkM5IDEwLjM0MzEgMTAuMzQzMSA5IDEyIDlaIiBmaWxsPSIjMWUxZTFlIi8+PC9zdmc+" alt="Cartoon coin" className="w-16 h-16" />
              </div>
            )}
            <div className="rounded-xl p-4" style={{ 
              backgroundColor: layoutStyle === 'gradient'
                ? (theme === 'dark' ? 'rgba(0, 0, 0, 0.3)' : 'rgba(0, 0, 0, 0.05)')
                : (theme === 'dark' ? '#252525' : '#f1f5f9')
            }}>
              <h3 className={`font-medium mb-2 ${theme === 'dark' ? 'text-white' : 'text-black'}`}>
                {t('tipOfTheDay')}
              </h3>
              <p className={theme === 'dark' ? 'text-white/70 text-sm' : 'text-black/70 text-sm'}>
                {t('tip1')}
              </p>
            </div>
          </div>
        </nav>
        
        {/* Content area with margin for sidebar on desktop */}
        <div className="flex-1 md:ml-20 lg:ml-64 p-2 overflow-hidden">
          <div className={`h-full rounded-lg overflow-hidden shadow-lg ${
            layoutStyle === 'modern' ? (theme === 'dark' ? 'bg-dark-lighter' : 'bg-white') : ''
          }`}>
            {activeTab === 'profile' && <UserProfile />}
            {activeTab === 'chat' && <ChatInterface />}
            {activeTab === 'dashboard' && <Dashboard />}
          </div>
        </div>
      </div>
      
      {/* Mobile navigation - fixed at the bottom, more compact */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 py-1 px-2 flex justify-around z-50" style={getMobileNavStyle()}>
        <button
          onClick={() => handleTabChange('profile')}
          className={`p-2 rounded-xl flex flex-col items-center transition-all duration-300 ${getMobileButtonStyle(activeTab === 'profile')}`}
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            className="h-5 w-5" 
            viewBox="0 0 20 20" 
            fill="currentColor"
          >
            <path 
              fillRule="evenodd" 
              d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" 
              clipRule="evenodd" 
            />
          </svg>
          <span className="text-xs mt-0.5">{t('profile')}</span>
        </button>
        
        <button
          onClick={() => handleTabChange('chat')}
          className={`p-2 rounded-xl flex flex-col items-center transition-all duration-300 ${getMobileButtonStyle(activeTab === 'chat')}`}
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            className="h-5 w-5" 
            viewBox="0 0 20 20" 
            fill="currentColor"
          >
            <path 
              fillRule="evenodd" 
              d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" 
              clipRule="evenodd" 
            />
          </svg>
          <span className="text-xs mt-0.5">{t('chat')}</span>
        </button>
        
        <button
          onClick={() => handleTabChange('dashboard')}
          className={`p-2 rounded-xl flex flex-col items-center transition-all duration-300 ${getMobileButtonStyle(activeTab === 'dashboard')}`}
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            className="h-5 w-5" 
            viewBox="0 0 20 20" 
            fill="currentColor"
          >
            <path 
              d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" 
            />
            <path 
              d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" 
            />
          </svg>
          <span className="text-xs mt-0.5">{t('dashboard')}</span>
        </button>
      </nav>
    </div>
  );
};

export default Layout; 