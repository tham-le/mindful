import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';

const PersonalityBadge = ({ mode }) => {
  const { t } = useLanguage();
  const { theme } = useTheme();
  
  if (!mode) return null;
  
  // Define colors for each personality mode
  const getColors = () => {
    switch(mode) {
      case 'nice':
        return {
          bg: theme === 'dark' ? 'rgba(79, 70, 229, 0.2)' : 'rgba(79, 70, 229, 0.15)',
          text: theme === 'dark' ? '#6366f1' : '#4338ca'
        };
      case 'funny':
        return {
          bg: theme === 'dark' ? 'rgba(245, 158, 11, 0.2)' : 'rgba(245, 158, 11, 0.15)',
          text: theme === 'dark' ? '#f59e0b' : '#d97706'
        };
      case 'irony':
        return {
          bg: theme === 'dark' ? 'rgba(236, 72, 153, 0.2)' : 'rgba(236, 72, 153, 0.15)',
          text: theme === 'dark' ? '#ec4899' : '#be185d'
        };
      default:
        return {
          bg: theme === 'dark' ? 'rgba(79, 70, 229, 0.2)' : 'rgba(79, 70, 229, 0.15)',
          text: theme === 'dark' ? '#6366f1' : '#4338ca'
        };
    }
  };
  
  const colors = getColors();
  
  return (
    <span 
      className="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
      style={{
        backgroundColor: colors.bg,
        color: colors.text
      }}
    >
      {t(mode)}
    </span>
  );
};

export default PersonalityBadge; 