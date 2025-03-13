import React from 'react';
import { useConversation } from '../context/ConversationContext';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';

const PersonalitySettings = ({ onClose }) => {
  const { personalityMode, setPersonalityMode } = useConversation();
  const { t } = useLanguage();
  const { theme } = useTheme();

  const personalities = [
    { id: 'nice', name: t('personalityNice'), description: t('personalityNiceDesc') },
    { id: 'direct', name: t('personalityDirect'), description: t('personalityDirectDesc') },
    { id: 'analytical', name: t('personalityAnalytical'), description: t('personalityAnalyticalDesc') }
  ];

  return (
    <div className="rounded-lg p-4" style={{ 
      backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.3)' : 'rgba(255, 255, 255, 0.7)',
      color: 'var(--color-text-primary)'
    }}>
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-semibold">{t('personalitySettings')}</h3>
        <button 
          onClick={onClose}
          className="p-1 rounded-full"
          style={{ 
            backgroundColor: theme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)'
          }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
      
      <p className="text-sm mb-4" style={{ color: 'var(--color-text-secondary)' }}>
        {t('personalitySettingsDesc')}
      </p>
      
      <div className="space-y-3">
        {personalities.map(personality => (
          <button
            key={personality.id}
            className="w-full text-left p-3 rounded-lg transition-all duration-200"
            style={{ 
              backgroundColor: personalityMode === personality.id 
                ? 'var(--color-primary)' 
                : theme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)',
              color: personalityMode === personality.id 
                ? '#ffffff' 
                : 'var(--color-text-primary)',
              transform: personalityMode === personality.id ? 'scale(1.02)' : 'scale(1)',
              boxShadow: personalityMode === personality.id ? '0 4px 6px rgba(0, 0, 0, 0.1)' : 'none'
            }}
            onClick={() => setPersonalityMode(personality.id)}
          >
            <div className="font-medium">{personality.name}</div>
            <div className="text-sm mt-1" style={{ 
              color: personalityMode === personality.id 
                ? 'rgba(255, 255, 255, 0.8)' 
                : 'var(--color-text-secondary)'
            }}>
              {personality.description}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default PersonalitySettings; 