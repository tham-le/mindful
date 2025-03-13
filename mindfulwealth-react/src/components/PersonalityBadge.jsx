import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';

const PersonalityBadge = ({ mode }) => {
  const { t } = useLanguage();
  const { theme } = useTheme();
  
  if (!mode) return null;
  
  return (
    <span 
      className={`ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
        mode === 'nice' 
          ? 'bg-primary/20 text-primary' 
          : 'bg-pink-500/20 text-pink-500'
      }`}
      style={{
        backgroundColor: mode === 'nice' 
          ? theme === 'dark' ? 'rgba(79, 70, 229, 0.2)' : 'rgba(79, 70, 229, 0.15)'
          : theme === 'dark' ? 'rgba(236, 72, 153, 0.2)' : 'rgba(236, 72, 153, 0.15)',
        color: mode === 'nice'
          ? theme === 'dark' ? '#6366f1' : '#4338ca'
          : theme === 'dark' ? '#ec4899' : '#be185d'
      }}
    >
      {mode === 'nice' ? t('nice') : t('sarcastic')}
    </span>
  );
};

export default PersonalityBadge; 