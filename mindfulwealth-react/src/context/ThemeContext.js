import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const useTheme = () => useContext(ThemeContext);

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme || 'dark';
  });

  const [layoutStyle, setLayoutStyle] = useState(() => {
    const savedLayout = localStorage.getItem('layoutStyle');
    return savedLayout || 'gradient';
  });

  useEffect(() => {
    localStorage.setItem('theme', theme);
    
    // Apply theme to the document
    if (theme === 'dark') {
      document.documentElement.classList.add('dark-theme');
      document.documentElement.classList.remove('light-theme');
    } else {
      document.documentElement.classList.add('light-theme');
      document.documentElement.classList.remove('dark-theme');
    }
    
    // Make sure combined classes are updated
    updateCombinedClasses(theme, layoutStyle);
  }, [theme]);

  useEffect(() => {
    localStorage.setItem('layoutStyle', layoutStyle);
    
    // Apply layout style to the document
    document.documentElement.classList.remove('gradient-layout', 'modern-layout');
    document.documentElement.classList.add(`${layoutStyle}-layout`);
    
    // Make sure combined classes are updated
    updateCombinedClasses(theme, layoutStyle);
  }, [layoutStyle]);
  
  // Helper function to update combined theme+layout classes
  const updateCombinedClasses = (currentTheme, currentLayout) => {
    // Remove all combined classes
    document.documentElement.classList.remove(
      'modern-layout-dark-theme',
      'modern-layout-light-theme',
      'gradient-layout-dark-theme',
      'gradient-layout-light-theme'
    );
    
    // Add the correct combined class
    document.documentElement.classList.add(`${currentLayout}-layout-${currentTheme}-theme`);
    
    // Also add the individual classes to ensure backward compatibility
    document.documentElement.classList.add(`${currentLayout}-layout`);
    document.documentElement.classList.add(`${currentTheme}-theme`);
  };

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'dark' ? 'light' : 'dark');
  };

  return (
    <ThemeContext.Provider
      value={{
        theme,
        setTheme,
        toggleTheme,
        isDark: theme === 'dark',
        layoutStyle,
        setLayoutStyle,
        isGradient: layoutStyle === 'gradient'
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

export default ThemeContext; 