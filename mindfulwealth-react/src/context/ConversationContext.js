import React, { createContext, useContext, useState, useEffect } from 'react';

const ConversationContext = createContext();

export const useConversation = () => useContext(ConversationContext);

export const ConversationProvider = ({ children }) => {
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
  }, [personalityMode]);

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

    // Simulate AI response after a delay
    setTimeout(() => {
      // Generate a simple response based on the user's message
      let response;
      const lowerText = text.toLowerCase();
      
      if (lowerText.includes('hello') || lowerText.includes('hi')) {
        response = "Hello! How can I help you with your financial decisions today?";
      } else if (lowerText.includes('invest')) {
        response = "Investment is a great way to grow your wealth. Would you like some advice on investment strategies?";
      } else if (lowerText.includes('save') || lowerText.includes('saving')) {
        response = "Saving is fundamental to financial health. Have you considered setting up an emergency fund?";
      } else if (lowerText.includes('budget')) {
        response = "Creating a budget is an excellent step. Would you like some tips on effective budgeting?";
      } else if (lowerText.includes('debt')) {
        response = "Managing debt is important. There are several strategies like the snowball or avalanche method that can help you pay off debt efficiently.";
      } else if (lowerText.includes('retirement')) {
        response = "Planning for retirement early can make a huge difference. Have you started contributing to a retirement account?";
      } else {
        response = "That's an interesting point. Would you like to explore this topic further in relation to your financial goals?";
      }

      // Add bot response
      const botMessage = {
        sender: 'bot',
        text: response,
        timestamp: new Date().toISOString(),
        personalityMode: personalityMode,
      };
      addMessage(botMessage);
      
      // Hide typing indicator
      setIsTyping(false);
    }, 1500); // Simulate thinking time
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