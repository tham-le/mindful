import React from 'react';
import { useConversation } from '../context/ConversationContext';
import PersonalityToggle from './PersonalityToggle';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';

const ChatHeader = () => {
  const { personalityMode } = useConversation();
  const { t } = useLanguage();
  const { theme } = useTheme();
  
  return (
    <div className="chat-header p-4 flex justify-between items-center" style={{
      backgroundColor: theme === 'dark' ? 'var(--color-bg-secondary)' : 'var(--color-bg-secondary)',
      borderBottom: `1px solid ${theme === 'dark' ? 'var(--color-border)' : 'var(--color-border)'}`
    }}>
      <div className="flex items-center">
        <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div className="ml-3">
          <h2 className="font-bold">{t('mindfulWealth')}</h2>
          <p className="text-xs opacity-70">{t('assistantDescription')}</p>
        </div>
      </div>
      
      <PersonalityToggle currentMode={personalityMode} />
    </div>
  );
};

export default ChatHeader; 