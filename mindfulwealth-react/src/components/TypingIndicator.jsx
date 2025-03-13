import React from 'react';
import { useTheme } from '../context/ThemeContext';

const TypingIndicator = () => {
  const { theme } = useTheme();
  
  return (
    <div className="flex items-center justify-center">
      <span 
        className="h-2 w-2 rounded-full inline-block mx-0.5 animate-bounce" 
        style={{ 
          animationDelay: '0ms',
          backgroundColor: theme === 'dark' ? 'var(--color-button-bg)' : 'var(--color-button-bg)'
        }}
      ></span>
      <span 
        className="h-2 w-2 rounded-full inline-block mx-0.5 animate-bounce" 
        style={{ 
          animationDelay: '200ms',
          backgroundColor: theme === 'dark' ? 'var(--color-button-bg)' : 'var(--color-button-bg)'
        }}
      ></span>
      <span 
        className="h-2 w-2 rounded-full inline-block mx-0.5 animate-bounce" 
        style={{ 
          animationDelay: '400ms',
          backgroundColor: theme === 'dark' ? 'var(--color-button-bg)' : 'var(--color-button-bg)'
        }}
      ></span>
    </div>
  );
};

export default TypingIndicator; 