import React from 'react';
import { ConversationProvider } from './context/ConversationContext';
import { ThemeProvider } from './context/ThemeContext';
import { LanguageProvider } from './context/LanguageContext';
import Layout from './components/Layout';
import './index.css';

function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <ConversationProvider>
          <Layout />
        </ConversationProvider>
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App; 