import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatInterface from '../components/ChatInterface';
import { ConversationProvider } from '../context/ConversationContext';
import { ThemeProvider } from '../context/ThemeContext';
import { LanguageProvider } from '../context/LanguageContext';
import api from '../services/api';

// Mock the API service
jest.mock('../services/api');

// Mock the useLanguage hook
jest.mock('../context/LanguageContext', () => {
  const originalModule = jest.requireActual('../context/LanguageContext');
  return {
    ...originalModule,
    useLanguage: () => ({
      t: (key) => key, // Return the key as the translation
    }),
  };
});

// Mock the useTheme hook
jest.mock('../context/ThemeContext', () => {
  const originalModule = jest.requireActual('../context/ThemeContext');
  return {
    ...originalModule,
    useTheme: () => ({
      theme: 'dark',
      isDark: true,
    }),
  };
});

describe('ChatInterface Component', () => {
  // Mock API response
  const mockChatResponse = {
    response: 'I see you want to buy shoes for 100€. Would you like to save this money instead? If you invested this amount, it could grow to 108€ in one year and 146.93€ in five years.',
    financial_data: {
      type: 'impulse',
      amount: 100.0,
      category: 'shoes',
      potential_value_1yr: 108.0,
      potential_value_5yr: 146.93
    }
  };

  // Mock investment response
  const mockInvestmentResponse = {
    response: 'For 1000€, I recommend investing in a low-cost index ETF that tracks the global market. This provides diversification and has historically returned around 8% annually.',
    financial_data: {
      type: 'investment',
      amount: 1000.0,
      potential_value_1yr: 1080.0,
      potential_value_5yr: 1469.3
    }
  };

  beforeEach(() => {
    // Reset all mocks
    jest.clearAllMocks();
    
    // Mock the API calls
    api.sendMessage.mockResolvedValue({ data: mockChatResponse });
  });

  test('renders chat interface with input field and send button', () => {
    render(
      <ThemeProvider>
        <LanguageProvider>
          <ConversationProvider>
            <ChatInterface />
          </ConversationProvider>
        </LanguageProvider>
      </ThemeProvider>
    );

    // Check that the input field and send button are rendered
    expect(screen.getByPlaceholderText('typeMessage')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'send' })).toBeInTheDocument();
  });

  test('sends message and displays response', async () => {
    render(
      <ThemeProvider>
        <LanguageProvider>
          <ConversationProvider>
            <ChatInterface />
          </ConversationProvider>
        </LanguageProvider>
      </ThemeProvider>
    );

    // Type a message
    const inputField = screen.getByPlaceholderText('typeMessage');
    fireEvent.change(inputField, { target: { value: 'I want to buy shoes for 100€' } });

    // Send the message
    const sendButton = screen.getByRole('button', { name: 'send' });
    fireEvent.click(sendButton);

    // Check that the API was called with the correct parameters
    expect(api.sendMessage).toHaveBeenCalledWith(
      'I want to buy shoes for 100€',
      null,
      []
    );

    // Wait for the response to be displayed
    await waitFor(() => {
      expect(screen.getByText('I want to buy shoes for 100€')).toBeInTheDocument();
      expect(screen.getByText(mockChatResponse.response)).toBeInTheDocument();
    });

    // Check that the input field was cleared
    expect(inputField.value).toBe('');
  });

  test('handles investment questions', async () => {
    // Mock the API response for investment questions
    api.sendMessage.mockResolvedValue({ data: mockInvestmentResponse });

    render(
      <ThemeProvider>
        <LanguageProvider>
          <ConversationProvider>
            <ChatInterface />
          </ConversationProvider>
        </LanguageProvider>
      </ThemeProvider>
    );

    // Type an investment question
    const inputField = screen.getByPlaceholderText('typeMessage');
    fireEvent.change(inputField, { target: { value: 'How should I invest 1000€?' } });

    // Send the message
    const sendButton = screen.getByRole('button', { name: 'send' });
    fireEvent.click(sendButton);

    // Check that the API was called with the correct parameters
    expect(api.sendMessage).toHaveBeenCalledWith(
      'How should I invest 1000€?',
      null,
      []
    );

    // Wait for the response to be displayed
    await waitFor(() => {
      expect(screen.getByText('How should I invest 1000€?')).toBeInTheDocument();
      expect(screen.getByText(mockInvestmentResponse.response)).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    // Mock API error
    api.sendMessage.mockRejectedValue(new Error('Failed to send message'));

    render(
      <ThemeProvider>
        <LanguageProvider>
          <ConversationProvider>
            <ChatInterface />
          </ConversationProvider>
        </LanguageProvider>
      </ThemeProvider>
    );

    // Type a message
    const inputField = screen.getByPlaceholderText('typeMessage');
    fireEvent.change(inputField, { target: { value: 'Test message' } });

    // Send the message
    const sendButton = screen.getByRole('button', { name: 'send' });
    fireEvent.click(sendButton);

    // Wait for the error message to be displayed
    await waitFor(() => {
      expect(screen.getByText('Test message')).toBeInTheDocument();
      expect(screen.getByText('errorSendingMessage')).toBeInTheDocument();
    });
  });

  test('displays typing indicator while waiting for response', async () => {
    // Create a delayed promise to simulate a slow API response
    api.sendMessage.mockImplementation(() => {
      return new Promise(resolve => {
        setTimeout(() => {
          resolve({ data: mockChatResponse });
        }, 1000);
      });
    });

    render(
      <ThemeProvider>
        <LanguageProvider>
          <ConversationProvider>
            <ChatInterface />
          </ConversationProvider>
        </LanguageProvider>
      </ThemeProvider>
    );

    // Type a message
    const inputField = screen.getByPlaceholderText('typeMessage');
    fireEvent.change(inputField, { target: { value: 'Test message' } });

    // Send the message
    const sendButton = screen.getByRole('button', { name: 'send' });
    fireEvent.click(sendButton);

    // Check that the typing indicator is displayed
    expect(screen.getByText('typing')).toBeInTheDocument();

    // Wait for the response to be displayed
    await waitFor(() => {
      expect(screen.getByText(mockChatResponse.response)).toBeInTheDocument();
    });

    // Check that the typing indicator is no longer displayed
    expect(screen.queryByText('typing')).not.toBeInTheDocument();
  });
}); 