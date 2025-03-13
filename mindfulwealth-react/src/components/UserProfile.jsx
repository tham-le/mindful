import React, { useState, useEffect } from 'react';
import { useConversation } from '../context/ConversationContext';
import { useTheme } from '../context/ThemeContext';
import { useLanguage } from '../context/LanguageContext';

const UserProfile = () => {
  const { personalityMode, setPersonalityMode, clearConversation } = useConversation();
  const { theme, setTheme, layoutStyle, setLayoutStyle } = useTheme();
  const { language, changeLanguage, t } = useLanguage();
  
  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);
  
  // Mock user data - in a real app, this would come from a user context or API
  const [userData, setUserData] = useState({
    name: 'Alex Johnson',
    email: 'alex.johnson@example.com',
    currency: 'EUR',
    savingsGoal: 500,
    monthlyBudget: 2000,
    notifications: true
  });

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setUserData({
      ...userData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleClearHistory = () => {
    if (window.confirm(t('clearConfirm'))) {
      clearConversation();
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">{t('userSettings')}</h1>
        
        <div className="glass-card p-6 mb-6">
          <div className="flex items-center mb-6">
            <div className="w-20 h-20 rounded-full bg-primary/20 flex items-center justify-center text-primary text-2xl font-bold">
              {userData.name.split(' ').map(n => n[0]).join('')}
            </div>
            <div className="ml-4">
              <h2 className="text-xl font-semibold">{userData.name}</h2>
              <p className="opacity-70">{userData.email}</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block opacity-70 text-sm font-medium mb-2">
                {t('name')}
              </label>
              <input
                type="text"
                name="name"
                value={userData.name}
                onChange={handleInputChange}
                className="w-full border rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary/50"
                style={{
                  backgroundColor: 'var(--color-bg-tertiary)',
                  color: 'var(--color-text-primary)',
                  borderColor: 'var(--color-border)'
                }}
              />
            </div>
            
            <div>
              <label className="block opacity-70 text-sm font-medium mb-2">
                {t('email')}
              </label>
              <input
                type="email"
                name="email"
                value={userData.email}
                onChange={handleInputChange}
                className="w-full border rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary/50"
                style={{
                  backgroundColor: 'var(--color-bg-tertiary)',
                  color: 'var(--color-text-primary)',
                  borderColor: 'var(--color-border)'
                }}
              />
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">{t('financialSettings')}</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block opacity-70 text-sm font-medium mb-2">
                {t('preferredCurrency')}
              </label>
              <select
                name="currency"
                value={userData.currency}
                onChange={handleInputChange}
                className="w-full border rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary/50"
                style={{
                  backgroundColor: 'var(--color-bg-tertiary)',
                  color: 'var(--color-text-primary)',
                  borderColor: 'var(--color-border)'
                }}
              >
                <option value="EUR">Euro (€)</option>
                <option value="USD">US Dollar ($)</option>
                <option value="GBP">British Pound (£)</option>
              </select>
            </div>
            
            <div>
              <label className="block opacity-70 text-sm font-medium mb-2">
                {t('monthlySavingsGoal')}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none opacity-70">
                  <span>
                    {userData.currency === 'EUR' ? '€' : userData.currency === 'USD' ? '$' : '£'}
                  </span>
                </div>
                <input
                  type="number"
                  name="savingsGoal"
                  value={userData.savingsGoal}
                  onChange={handleInputChange}
                  className="w-full border rounded-md py-2 pl-8 pr-3 focus:outline-none focus:ring-2 focus:ring-primary/50"
                  style={{
                    backgroundColor: 'var(--color-bg-tertiary)',
                    color: 'var(--color-text-primary)',
                    borderColor: 'var(--color-border)'
                  }}
                />
              </div>
            </div>
            
            <div>
              <label className="block opacity-70 text-sm font-medium mb-2">
                {t('monthlyBudget')}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none opacity-70">
                  <span>
                    {userData.currency === 'EUR' ? '€' : userData.currency === 'USD' ? '$' : '£'}
                  </span>
                </div>
                <input
                  type="number"
                  name="monthlyBudget"
                  value={userData.monthlyBudget}
                  onChange={handleInputChange}
                  className="w-full border rounded-md py-2 pl-8 pr-3 focus:outline-none focus:ring-2 focus:ring-primary/50"
                  style={{
                    backgroundColor: 'var(--color-bg-tertiary)',
                    color: 'var(--color-text-primary)',
                    borderColor: 'var(--color-border)'
                  }}
                />
              </div>
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">{t('appSettings')}</h2>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="opacity-80">{t('assistantPersonality')}</label>
              <div className="bg-black/10 rounded-full p-1 flex items-center">
                {['nice', 'direct', 'analytical'].map(mode => (
                  <button
                    key={mode}
                    onClick={() => setPersonalityMode(mode)}
                    className={`px-3 py-1 rounded-full text-sm transition-colors duration-200 ${
                      personalityMode === mode
                        ? 'bg-primary text-white'
                        : 'opacity-70 hover:opacity-100'
                    }`}
                  >
                    {t('personality' + mode.charAt(0).toUpperCase() + mode.slice(1))}
                  </button>
                ))}
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <label className="opacity-80">{t('enableNotifications')}</label>
              <div className="relative inline-block w-10 mr-2 align-middle select-none">
                <input
                  type="checkbox"
                  name="notifications"
                  id="notifications"
                  checked={userData.notifications}
                  onChange={handleInputChange}
                  className="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                />
                <label
                  htmlFor="notifications"
                  className={`toggle-label block overflow-hidden h-6 rounded-full cursor-pointer ${
                    userData.notifications ? 'bg-primary' : 'bg-gray-600'
                  }`}
                ></label>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <label className="opacity-80">{t('theme')}</label>
              <div className="bg-black/10 rounded-full p-1 flex items-center">
                <button
                  onClick={() => setTheme('dark')}
                  className={`px-3 py-1 rounded-full text-sm transition-colors duration-200 ${
                    theme === 'dark'
                      ? 'bg-primary text-white'
                      : 'opacity-70 hover:opacity-100'
                  }`}
                >
                  {t('dark')}
                </button>
                <div className="mx-1 opacity-50">|</div>
                <button
                  onClick={() => setTheme('light')}
                  className={`px-3 py-1 rounded-full text-sm transition-colors duration-200 ${
                    theme === 'light'
                      ? 'bg-primary text-white'
                      : 'opacity-70 hover:opacity-100'
                  }`}
                >
                  {t('light')}
                </button>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <label className="opacity-80">{t('layoutStyle')}</label>
              <div className="bg-black/10 rounded-full p-1 flex items-center">
                <button
                  onClick={() => setLayoutStyle('gradient')}
                  className={`px-3 py-1 rounded-full text-sm transition-colors duration-200 ${
                    layoutStyle === 'gradient'
                      ? 'bg-primary text-white'
                      : 'opacity-70 hover:opacity-100'
                  }`}
                >
                  {t('gradient')}
                </button>
                <div className="mx-1 opacity-50">|</div>
                <button
                  onClick={() => setLayoutStyle('modern')}
                  className={`px-3 py-1 rounded-full text-sm transition-colors duration-200 ${
                    layoutStyle === 'modern'
                      ? 'bg-primary text-white'
                      : 'opacity-70 hover:opacity-100'
                  }`}
                >
                  {t('modern')}
                </button>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <label className="opacity-80">{t('language')}</label>
              <div className="bg-black/10 rounded-full p-1 flex items-center">
                <button
                  onClick={() => changeLanguage('en')}
                  className={`px-3 py-1 rounded-full text-sm transition-colors duration-200 ${
                    language === 'en'
                      ? 'bg-primary text-white'
                      : 'opacity-70 hover:opacity-100'
                  }`}
                >
                  {t('english')}
                </button>
                <div className="mx-1 opacity-50">|</div>
                <button
                  onClick={() => changeLanguage('fr')}
                  className={`px-3 py-1 rounded-full text-sm transition-colors duration-200 ${
                    language === 'fr'
                      ? 'bg-primary text-white'
                      : 'opacity-70 hover:opacity-100'
                  }`}
                >
                  {t('french')}
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6">
          <h2 className="text-xl font-semibold mb-4">{t('privacy')}</h2>
          
          <div className="space-y-4">
            <button
              onClick={handleClearHistory}
              className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200"
            >
              {t('clearHistory')}
            </button>
            
            <p className="opacity-70 text-sm">
              {t('clearHistoryWarning')}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile; 