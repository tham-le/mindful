import React from 'react';
import { useConversation } from '../context/ConversationContext';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';
import api from '../services/api';

const PersonalityToggle = ({ currentMode }) => {
  const { setPersonalityMode, addMessage } = useConversation();
  const { t } = useLanguage();
  const { theme } = useTheme();

  const handleToggle = async (mode) => {
    if (mode !== currentMode) {
      try {
        // Set the personality mode immediately for better UX
        setPersonalityMode(mode);
        
        // Add a message from the bot indicating the mode change
        let switchMessage = '';
        if (mode === 'nice') {
          switchMessage = t('switchedToNice');
        } else if (mode === 'funny') {
          switchMessage = t('switchedToFunny');
        } else if (mode === 'irony') {
          switchMessage = t('switchedToIrony');
        }
        
        addMessage({
          sender: 'bot',
          text: switchMessage,
          timestamp: new Date().toISOString(),
          personalityMode: mode, // Add the personality mode to the message
        });
        
        // Try to call the API, but don't block the UI update
        try {
          await api.setPersonalityMode(mode);
        } catch (apiError) {
          console.error('API call failed, but UI was updated:', apiError);
          // The UI is already updated, so we don't need to handle this error
        }
      } catch (error) {
        console.error('Error setting personality mode:', error);
      }
    }
  };

  return (
    <div className="personality-toggle">
      <div className="flex items-center">
        <span className="text-xs opacity-70 mr-2">{t('personality')}:</span>
        <div 
          className="rounded-full p-1 flex items-center"
          style={{
            backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.2)' : 'rgba(0, 0, 0, 0.05)'
          }}
        >
          {['nice', 'funny', 'irony'].map((mode, index) => (
            <React.Fragment key={mode}>
              {index > 0 && (
                <div className="mx-1" style={{ opacity: theme === 'dark' ? 0.5 : 0.3 }}>|</div>
              )}
              <button
                onClick={() => handleToggle(mode)}
                className={`px-3 py-1 rounded-full text-xs transition-colors duration-200 ${
                  currentMode === mode
                    ? 'bg-primary text-white'
                    : 'opacity-70 hover:opacity-100'
                }`}
                style={{
                  backgroundColor: currentMode === mode ? 'var(--color-primary)' : 'transparent',
                  color: currentMode === mode 
                    ? 'white' 
                    : theme === 'dark' ? 'var(--color-text-primary)' : 'var(--color-text-primary)'
                }}
              >
                {t(mode)}
              </button>
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PersonalityToggle; 