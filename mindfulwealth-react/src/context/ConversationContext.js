import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from './AuthContext';

const ConversationContext = createContext();

export const useConversation = () => useContext(ConversationContext);

export const ConversationProvider = ({ children }) => {
  const { user } = useAuth() || { user: null };
  
  // Messages state
  const [messages, setMessages] = useState(() => {
    const savedMessages = localStorage.getItem('chatHistory');
    if (savedMessages) {
      try {
        return JSON.parse(savedMessages);
      } catch (e) {
        console.error('Error parsing saved messages:', e);
        return defaultMessages;
      }
    }
    return defaultMessages;
  });

  // Conversation context state
  const [conversationContext, setConversationContext] = useState(() => {
    const savedContext = localStorage.getItem('chatContext');
    if (savedContext) {
      try {
        return {
          ...defaultContext,
          ...JSON.parse(savedContext)
        };
      } catch (e) {
        console.error('Error parsing saved context:', e);
        return defaultContext;
      }
    }
    return defaultContext;
  });

  // Personality mode state
  const [personalityMode, setPersonalityMode] = useState(() => {
    // First try to get from user preferences
    if (user?.personality_preference) {
      return user.personality_preference;
    }
    // Then try to get from localStorage
    const savedMode = localStorage.getItem('personalityMode');
    return savedMode || 'nice';
  });
  
  // Loading state
  const [isTyping, setIsTyping] = useState(false);

  // Save to localStorage when messages or context changes
  useEffect(() => {
    localStorage.setItem('chatHistory', JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    localStorage.setItem('chatContext', JSON.stringify(conversationContext));
  }, [conversationContext]);

  // Save personality mode to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('personalityMode', personalityMode);
    
    // Update on the backend
    api.setPersonalityMode(personalityMode)
      .catch(error => console.error('Error setting personality mode:', error));
  }, [personalityMode]);

  // Update personality mode when user changes
  useEffect(() => {
    if (user && user.personality_preference && user.personality_preference !== personalityMode) {
      setPersonalityMode(user.personality_preference);
    }
  }, [user, personalityMode]);

  // Add a message to the conversation
  const addMessage = (message) => {
    setMessages(prevMessages => [...prevMessages, message]);
  };

  // Send a message and get a response
  const sendMessage = async (text) => {
    if (!text.trim()) return;

    // Add user message
    const userMessage = {
      sender: 'user',
      text: text.trim(),
      timestamp: new Date().toISOString(),
    };
    addMessage(userMessage);

    // Show typing indicator
    setIsTyping(true);

    try {
      // Format conversation history for API
      const formattedHistory = messages.map(msg => ({
        isUser: msg.sender === 'user',
        text: msg.text,
        timestamp: msg.timestamp
      }));

      // Call API to get response
      const response = await api.sendMessage(text, conversationContext, formattedHistory);
      
      // Process API response
      if (response && response.data) {
        const botMessage = {
          sender: 'bot',
          text: response.data.response,
          timestamp: new Date().toISOString(),
          personalityMode: personalityMode,
          financialData: response.data.financial_data
        };
        
        // Add bot response to messages
        addMessage(botMessage);
        
        // Update context with financial data if present
        if (response.data.financial_data) {
          updateContext({
            lastMentionedAmount: response.data.financial_data.original?.amount,
            lastMentionedCurrency: response.data.financial_data.original?.currency,
            lastResponseTime: new Date().toISOString()
          });
        }
      } else {
        // Fallback for no response
        const fallbackMessage = {
          sender: 'bot',
          text: "I'm sorry, I couldn't process your request at the moment. Please try again later.",
          timestamp: new Date().toISOString(),
          personalityMode: personalityMode,
        };
        addMessage(fallbackMessage);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage = {
        sender: 'bot',
        text: "I'm having trouble connecting to the server. Please check your connection and try again.",
        timestamp: new Date().toISOString(),
        personalityMode: personalityMode,
        isError: true
      };
      addMessage(errorMessage);
    } finally {
      // Hide typing indicator
      setIsTyping(false);
    }
  };

  // Update conversation context
  const updateContext = (newContext) => {
    setConversationContext(prevContext => ({
      ...prevContext,
      ...newContext
    }));
  };

  // Check if there's an active financial context
  const hasActiveFinancialContext = () => {
    return (
      conversationContext.lastMentionedAmount !== null &&
      conversationContext.lastMentionedItem !== null &&
      conversationContext.ongoingDiscussion === true
    );
  };

  // Clear conversation history
  const clearConversation = () => {
    setMessages(defaultMessages);
    setConversationContext(defaultContext);
    localStorage.removeItem('chatHistory');
    localStorage.removeItem('chatContext');
  };

  return (
    <ConversationContext.Provider
      value={{
        messages,
        setMessages,
        addMessage,
        sendMessage,
        conversationContext,
        updateContext,
        personalityMode,
        setPersonalityMode,
        isTyping,
        setIsTyping,
        hasActiveFinancialContext,
        clearConversation
      }}
    >
      {children}
    </ConversationContext.Provider>
  );
};

// Default values
const defaultMessages = [
  {
    sender: 'bot',
    text: "Hello! I'm your MindfulWealth assistant. How can I help you with your financial decisions today?",
    timestamp: new Date().toISOString(),
    personalityMode: 'nice',
  }
];

const defaultContext = {
  // Current financial context
  lastMentionedAmount: null,
  lastMentionedCurrency: null,
  lastMentionedItem: null,
  lastDetectedType: null, // "impulse" or "reasonable"
  ongoingDiscussion: false,

  // Historical context
  discussionStartTime: null,
  lastResponseTime: null,
  mentionedItems: [],
  mentionedAmounts: [],

  // Conversation flow
  followUpQuestions: [],
  userResponses: [],
}; 