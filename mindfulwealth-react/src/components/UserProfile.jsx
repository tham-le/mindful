import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { useLanguage } from '../context/LanguageContext';
import { useConversation } from '../context/ConversationContext';

const UserProfile = () => {
  const { user, logout, updateProfile, updatePreferences } = useAuth();
  const { theme, setTheme, layoutStyle, setLayoutStyle } = useTheme();
  const { t, language, changeLanguage } = useLanguage();
  const { personalityMode, setPersonalityMode } = useConversation();
  
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState('');
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);

  useEffect(() => {
    if (user) {
      setName(user.name || '');
    }
  }, [user]);

  const handleSubmit = (e) => {
    e.preventDefault();
    updateProfile({ name });
    setIsEditing(false);
  };

  const handleLogout = () => {
    setShowLogoutConfirm(true);
  };

  const confirmLogout = () => {
    logout();
  };

  const cancelLogout = () => {
    setShowLogoutConfirm(false);
  };
  
  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
    // Save preference to backend
    updatePreferences({ theme_preference: newTheme });
  };
  
  const handleLayoutChange = (newLayout) => {
    setLayoutStyle(newLayout);
    // Save preference to backend
    updatePreferences({ layout_preference: newLayout });
  };
  
  const handleLanguageChange = (newLanguage) => {
    changeLanguage(newLanguage);
    // Save preference to backend
    updatePreferences({ language_preference: newLanguage });
  };
  
  const handlePersonalityChange = (newPersonality) => {
    setPersonalityMode(newPersonality);
    // Save preference to backend
    updatePreferences({ personality_preference: newPersonality });
  };

  if (!user) {
    return <div>Loading user profile...</div>;
  }

  return (
    <div className={`shadow rounded-lg p-6 ${theme === 'dark' ? 'bg-gray-800' : 'bg-white'}`}>
      <div className="flex justify-between items-center mb-6">
        <h2 className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>{t('profile')}</h2>
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
        >
          {t('logout')}
        </button>
      </div>

      {showLogoutConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className={`p-6 rounded-lg shadow-lg max-w-md w-full ${theme === 'dark' ? 'bg-gray-800' : 'bg-white'}`}>
            <h3 className={`text-xl font-bold mb-4 ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>{t('confirmLogout')}</h3>
            <p className={`mb-6 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>{t('logoutConfirmMessage')}</p>
            <div className="flex justify-end space-x-4">
              <button
                onClick={cancelLogout}
                className={`px-4 py-2 border rounded hover:bg-gray-100 ${theme === 'dark' ? 'border-gray-600 text-gray-300 hover:bg-gray-700' : 'border-gray-300 text-gray-700'}`}
              >
                {t('cancel')}
              </button>
              <button
                onClick={confirmLogout}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
              >
                {t('logout')}
              </button>
            </div>
          </div>
        </div>
      )}

      <div className={`p-4 rounded-lg mb-6 ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-50'}`}>
        <div className="flex items-center space-x-4">
          <div className="bg-indigo-100 p-3 rounded-full">
            <svg
              className="h-8 w-8 text-indigo-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
          </div>
          <div>
            <p className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>{t('accountType')}</p>
            <p className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>{user.is_demo ? t('demoUser') : t('registeredUser')}</p>
          </div>
        </div>
      </div>

      {isEditing ? (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="name" className={`block text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>
              {t('name')}
            </label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className={`mt-1 block w-full border rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 ${
                theme === 'dark' 
                  ? 'bg-gray-700 border-gray-600 text-white' 
                  : 'bg-white border-gray-300 text-gray-900'
              }`}
            />
          </div>
          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => setIsEditing(false)}
              className={`px-4 py-2 border rounded-md shadow-sm text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
                theme === 'dark'
                  ? 'border-gray-600 text-gray-300 bg-gray-700 hover:bg-gray-600'
                  : 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50'
              }`}
            >
              {t('cancel')}
            </button>
            <button
              type="submit"
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {t('save')}
            </button>
          </div>
        </form>
      ) : (
        <div className="space-y-6">
          <div className="space-y-4">
            <div>
              <p className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>{t('name')}</p>
              <p className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>{user.name}</p>
            </div>
            {user.email && (
              <div>
                <p className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>{t('email')}</p>
                <p className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>{user.email}</p>
              </div>
            )}
            <div>
              <p className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>{t('memberSince')}</p>
              <p className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>
                {new Date(user.created_at).toLocaleDateString()}
              </p>
            </div>
            <div>
              <p className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>{t('lastLogin')}</p>
              <p className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>
                {new Date(user.last_login).toLocaleDateString()}
              </p>
            </div>
            <button
              onClick={() => setIsEditing(true)}
              className={`mt-4 px-4 py-2 border rounded-md shadow-sm text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
                theme === 'dark'
                  ? 'border-gray-600 text-gray-300 bg-gray-700 hover:bg-gray-600'
                  : 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50'
              }`}
            >
              {t('editProfile')}
            </button>
          </div>
          
          {/* Appearance Settings */}
          <div className={`border-t pt-6 ${theme === 'dark' ? 'border-gray-700' : 'border-gray-200'}`}>
            <h3 className={`text-lg font-medium mb-4 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>{t('appearanceSettings')}</h3>
            
            {/* Theme Selection */}
            <div className="mb-6">
              <p className={`text-sm font-medium mb-2 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>{t('theme')}</p>
              <div className="flex space-x-4">
                <button
                  onClick={() => handleThemeChange('light')}
                  className={`px-4 py-2 rounded-md ${
                    theme === 'light'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {t('light')}
                </button>
                <button
                  onClick={() => handleThemeChange('dark')}
                  className={`px-4 py-2 rounded-md ${
                    theme === 'dark'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {t('dark')}
                </button>
              </div>
            </div>
            
            {/* Layout Selection */}
            <div className="mb-6">
              <p className={`text-sm font-medium mb-2 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>{t('layoutStyle')}</p>
              <div className="flex space-x-4">
                <button
                  onClick={() => handleLayoutChange('gradient')}
                  className={`px-4 py-2 rounded-md ${
                    layoutStyle === 'gradient'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {t('gradient')}
                </button>
                <button
                  onClick={() => handleLayoutChange('modern')}
                  className={`px-4 py-2 rounded-md ${
                    layoutStyle === 'modern'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {t('modern')}
                </button>
              </div>
            </div>
            
            {/* Language Selection */}
            <div className="mb-6">
              <p className={`text-sm font-medium mb-2 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>{t('language')}</p>
              <div className="flex space-x-4">
                <button
                  onClick={() => handleLanguageChange('en')}
                  className={`px-4 py-2 rounded-md ${
                    language === 'en'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {t('english')}
                </button>
                <button
                  onClick={() => handleLanguageChange('fr')}
                  className={`px-4 py-2 rounded-md ${
                    language === 'fr'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {t('french')}
                </button>
              </div>
            </div>
            
            {/* AI Personality Selection */}
            <div>
              <p className={`text-sm font-medium mb-2 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>{t('assistantPersonality')}</p>
              <div className="flex space-x-4">
                <button
                  onClick={() => handlePersonalityChange('nice')}
                  className={`px-4 py-2 rounded-md ${
                    personalityMode === 'nice'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {t('nice')}
                </button>
                <button
                  onClick={() => handlePersonalityChange('funny')}
                  className={`px-4 py-2 rounded-md ${
                    personalityMode === 'funny'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {t('funny')}
                </button>
                <button
                  onClick={() => handlePersonalityChange('irony')}
                  className={`px-4 py-2 rounded-md ${
                    personalityMode === 'irony'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {t('irony')}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserProfile; 