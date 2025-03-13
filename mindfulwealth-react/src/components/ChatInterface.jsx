import React, { useState, useRef, useEffect } from 'react';
import { useConversation } from '../context/ConversationContext';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';
import PersonalitySettings from './PersonalitySettings';

const ChatInterface = () => {
  const [message, setMessage] = useState('');
  const [showPersonality, setShowPersonality] = useState(false);
  const { messages, sendMessage, isTyping, personalityMode, setPersonalityMode, clearConversation } = useConversation();
  const { t } = useLanguage();
  const { theme, layoutStyle } = useTheme();
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);

  // Scroll to bottom when messages change or when typing status changes
  useEffect(() => {
    // Only auto-scroll if there are more than 2 messages or if user is at the bottom
    if (messages.length > 2) {
      scrollToBottom();
    } else if (messages.length > 0) {
      // For the first few messages, we want to ensure they're visible at the top
      messagesContainerRef.current?.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  }, [messages, isTyping]);

  // Clear local storage on component mount for testing
  useEffect(() => {
    // Uncomment the next line to clear chat history on page load (for testing)
    // clearConversation();
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      sendMessage(message);
      setMessage('');
    }
  };

  // Determine if we should position messages at the top or bottom
  const shouldPositionAtTop = messages.length < 3;

  return (
    <div className="flex flex-col h-full bg-opacity-80" style={{ 
      backgroundColor: 'var(--color-bg-primary)',
    }}>
      {/* Fixed header at the top - positioned below the app header */}
      <div className="fixed left-0 md:left-20 lg:left-64 right-0 z-20 border-b border-opacity-20" style={{ 
        top: "3.5rem", /* Height of app header only */
        borderColor: 'var(--color-border)',
        backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.2)' : 'rgba(255, 255, 255, 0.7)',
        backdropFilter: 'blur(8px)'
      }}>
        {/* Main header with title and clear button */}
        <div className="flex justify-between items-center p-4">
          <h2 className="text-xl font-semibold" style={{ color: 'var(--color-text-primary)' }}>
            {t('chatWithAI')}
          </h2>
          <button
            onClick={clearConversation}
            className="px-3 py-1 rounded-lg text-sm transition-colors duration-200"
            style={{ 
              backgroundColor: theme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)',
              color: 'var(--color-text-primary)'
            }}
          >
            {t('clearConversation')}
          </button>
        </div>
        
        {/* Personality panel - always visible */}
        <div className="px-4 py-2 border-t border-opacity-10" style={{ 
          borderColor: 'var(--color-border)',
          backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.1)' : 'rgba(0, 0, 0, 0.02)'
        }}>
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <span className="text-sm mr-2" style={{ color: 'var(--color-text-secondary)' }}>
                {t('personality')}:
              </span>
              <div className="flex rounded-lg overflow-hidden" style={{ 
                backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.2)' : 'rgba(0, 0, 0, 0.05)'
              }}>
                {['nice', 'direct', 'analytical'].map(mode => (
                  <button
                    key={mode}
                    className="px-3 py-1 text-sm transition-colors duration-200"
                    style={{ 
                      backgroundColor: personalityMode === mode 
                        ? 'var(--color-primary)' 
                        : 'transparent',
                      color: personalityMode === mode 
                        ? '#ffffff' 
                        : 'var(--color-text-primary)'
                    }}
                    onClick={() => setPersonalityMode(mode)}
                  >
                    {t('personality' + mode.charAt(0).toUpperCase() + mode.slice(1))}
                  </button>
                ))}
              </div>
            </div>
            
            <button
              onClick={() => setShowPersonality(!showPersonality)}
              className="p-2 rounded-full transition-colors duration-200"
              style={{ 
                backgroundColor: theme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)',
                color: 'var(--color-text-primary)'
              }}
              aria-label={t('personalitySettings')}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
          
          {/* Personality settings panel */}
          {showPersonality && (
            <div className="mt-2">
              <PersonalitySettings onClose={() => setShowPersonality(false)} />
            </div>
          )}
        </div>
      </div>
      
      {/* Empty space to push content below fixed header */}
      <div style={{ height: "110px" }}></div>
      
      {/* Messages container - scrollable */}
      <div 
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto p-4 space-y-4"
        style={{ 
          backgroundColor: 'var(--color-bg-secondary)',
          paddingBottom: '120px', // Increased padding to ensure last message is visible above input and nav bar
          display: 'flex',
          flexDirection: 'column',
          justifyContent: shouldPositionAtTop ? 'flex-start' : 'flex-end'
        }}
      >
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full">
            <div className="text-center max-w-md">
              <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--color-text-primary)' }}>
                {t('welcomeTitle')}
              </h2>
              <p className="opacity-70 mb-6" style={{ color: 'var(--color-text-secondary)' }}>
                {t('welcomeMessage')}
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {[
                  t('sampleQuestion1'),
                  t('sampleQuestion2'),
                  t('sampleQuestion3'),
                  t('sampleQuestion4')
                ].map((question, index) => (
                  <button
                    key={index}
                    className="p-3 text-left rounded-lg transition-colors duration-200"
                    style={{ 
                      backgroundColor: theme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)',
                      color: 'var(--color-text-primary)'
                    }}
                    onClick={() => {
                      setMessage(question);
                      setTimeout(() => {
                        handleSubmit({ preventDefault: () => {} });
                      }, 100);
                    }}
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className={`space-y-4 ${shouldPositionAtTop ? 'mt-0' : 'mt-auto'}`}>
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-3 ${
                    msg.sender === 'user'
                      ? 'rounded-tr-none'
                      : 'rounded-tl-none'
                  }`}
                  style={{
                    backgroundColor:
                      msg.sender === 'user'
                        ? 'var(--color-user-message)'
                        : 'var(--color-bot-message)',
                    color:
                      msg.sender === 'user'
                        ? 'var(--color-user-message-text)'
                        : 'var(--color-bot-message-text)',
                    boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)'
                  }}
                >
                  <p className="whitespace-pre-wrap break-words">{msg.text}</p>
                  {msg.sender === 'bot' && msg.personalityMode && (
                    <div className="mt-2">
                      <span 
                        className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                        style={{
                          backgroundColor: layoutStyle === 'modern' 
                            ? `var(--modern-color-primary-light, var(--color-primary-light))` 
                            : 'var(--color-primary-light)',
                          color: layoutStyle === 'modern' 
                            ? `var(--modern-color-primary, var(--color-primary))` 
                            : 'var(--color-primary)'
                        }}
                      >
                        {t('personality' + msg.personalityMode.charAt(0).toUpperCase() + msg.personalityMode.slice(1))}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
        
        {/* Typing indicator */}
        {isTyping && (
          <div className="flex justify-start">
            <div
              className="max-w-[80%] rounded-lg p-3 rounded-tl-none"
              style={{
                backgroundColor: 'var(--color-bot-message)',
                color: 'var(--color-bot-message-text)',
                boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)'
              }}
            >
              <div className="flex space-x-1">
                <div className="w-2 h-2 rounded-full animate-bounce" style={{ backgroundColor: 'var(--color-bot-message-text)', animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 rounded-full animate-bounce" style={{ backgroundColor: 'var(--color-bot-message-text)', animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 rounded-full animate-bounce" style={{ backgroundColor: 'var(--color-bot-message-text)', animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}
        
        {/* Invisible element to scroll to */}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Message input - fixed at the bottom, adjusted for desktop sidebar and mobile footer */}
      <div 
        className="fixed left-0 md:left-20 lg:left-64 right-0 p-4 border-t border-opacity-20 z-20 md:bottom-0" 
        style={{ 
          borderColor: 'var(--color-border)',
          backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.2)' : 'rgba(255, 255, 255, 0.7)',
          backdropFilter: 'blur(8px)',
          bottom: "4.5rem" /* Increased space above mobile navigation */
        }}
      >
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={t('typeMessage')}
            className="flex-1 p-3 rounded-lg focus:outline-none focus:ring-2 transition-all duration-200"
            style={{ 
              backgroundColor: theme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)',
              color: 'var(--color-text-primary)',
              borderColor: 'var(--color-border)'
            }}
          />
          <button
            type="submit"
            className="p-3 rounded-lg transition-colors duration-200 flex items-center justify-center"
            style={{ 
              backgroundColor: layoutStyle === 'modern' 
                ? 'var(--modern-color-primary, var(--color-primary))' 
                : 'var(--color-primary)',
              color: '#ffffff'
            }}
            disabled={!message.trim()}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
            </svg>
          </button>
        </form>
      </div>
      
      {/* Empty space to push content above fixed input and mobile navigation */}
      <div className="md:hidden" style={{ height: "150px" }}></div>
      <div className="hidden md:block" style={{ height: "70px" }}></div>
    </div>
  );
};

export default ChatInterface; 