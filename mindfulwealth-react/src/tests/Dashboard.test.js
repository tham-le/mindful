import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Dashboard from '../components/Dashboard';
import api from '../services/api';
import { ThemeProvider } from '../context/ThemeContext';
import { LanguageProvider } from '../context/LanguageContext';

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

// Mock the chart.js library
jest.mock('chart.js');
jest.mock('react-chartjs-2', () => ({
  Doughnut: () => <div data-testid="mock-doughnut-chart">Doughnut Chart</div>,
  Line: () => <div data-testid="mock-line-chart">Line Chart</div>,
}));

// Mock the heroicons
jest.mock('@heroicons/react/24/outline', () => ({
  BanknotesIcon: () => <div data-testid="mock-banknotes-icon">BanknotesIcon</div>,
  ArrowTrendingUpIcon: () => <div data-testid="mock-arrow-trending-up-icon">ArrowTrendingUpIcon</div>,
  ArrowTrendingDownIcon: () => <div data-testid="mock-arrow-trending-down-icon">ArrowTrendingDownIcon</div>,
  ChartBarIcon: () => <div data-testid="mock-chart-bar-icon">ChartBarIcon</div>,
  CurrencyDollarIcon: () => <div data-testid="mock-currency-dollar-icon">CurrencyDollarIcon</div>,
}));

describe('Dashboard Component', () => {
  // Mock dashboard data
  const mockDashboardData = {
    summary: {
      total_balance: 24563.00,
      monthly_income: 8350.00,
      monthly_expenses: 5240.00,
      savingsRate: 37.2,
      savingsRate_change_pct: 3.1,
      total_spent: 5240.00,
      total_budget: 8000.00,
      budget_remaining: 2760.00,
      budget_remaining_pct: 34.5,
      spending_change_pct: -0.5,
      total_saved: 1200.00,
      potential_growth_1yr: 1296.00,
      potential_growth_5yr: 1762.00
    },
    portfolio: {
      total: 24563.00,
      allocation: {
        stocks: 45,
        bonds: 30,
        cash: 25
      }
    },
    activity: [
      {
        id: 1,
        title: 'Salary Deposit',
        time: 'Today, 10:30 AM',
        amount: 3500.00,
        type: 'deposit'
      },
      {
        id: 2,
        title: 'Rent Payment',
        time: 'Yesterday, 2:15 PM',
        amount: 1200.00,
        type: 'withdrawal'
      }
    ],
    goals: [
      {
        name: 'Emergency Fund',
        current: 7500,
        target: 10000,
        progress: 75
      },
      {
        name: 'Vacation Savings',
        current: 1350,
        target: 3000,
        progress: 45
      }
    ],
    insights: [
      {
        type: 'positive',
        title: 'Positive Trend',
        description: 'Your savings rate has increased by 3.1% compared to last month. Keep up the good work!'
      },
      {
        type: 'suggestion',
        title: 'Suggestion',
        description: 'Consider increasing your retirement contributions to maximize tax benefits.'
      }
    ]
  };

  beforeEach(() => {
    // Reset all mocks
    jest.clearAllMocks();
    
    // Mock the API calls
    api.getDashboard.mockResolvedValue({ data: mockDashboardData });
  });

  test('renders dashboard with all sections', async () => {
    render(
      <ThemeProvider>
        <LanguageProvider>
          <Dashboard />
        </LanguageProvider>
      </ThemeProvider>
    );

    // Wait for the API call to resolve
    await waitFor(() => {
      expect(api.getDashboard).toHaveBeenCalledTimes(1);
    });

    // Check that all sections are rendered
    expect(screen.getByText('totalBalance')).toBeInTheDocument();
    expect(screen.getByText('monthlyIncome')).toBeInTheDocument();
    expect(screen.getByText('monthlyExpenses')).toBeInTheDocument();
    expect(screen.getByText('savingsRate')).toBeInTheDocument();
    
    // Check that the portfolio section is rendered
    expect(screen.getByText('portfolioOverview')).toBeInTheDocument();
    
    // Check that the activity section is rendered
    expect(screen.getByText('recentActivity')).toBeInTheDocument();
    expect(screen.getByText('Salary Deposit')).toBeInTheDocument();
    expect(screen.getByText('Rent Payment')).toBeInTheDocument();
    
    // Check that the goals section is rendered
    expect(screen.getByText('financialGoals')).toBeInTheDocument();
    expect(screen.getByText('Emergency Fund')).toBeInTheDocument();
    expect(screen.getByText('Vacation Savings')).toBeInTheDocument();
    
    // Check that the insights section is rendered
    expect(screen.getByText('financialInsights')).toBeInTheDocument();
    expect(screen.getByText('Positive Trend')).toBeInTheDocument();
    expect(screen.getByText('Suggestion')).toBeInTheDocument();
  });

  test('displays correct financial values', async () => {
    render(
      <ThemeProvider>
        <LanguageProvider>
          <Dashboard />
        </LanguageProvider>
      </ThemeProvider>
    );

    // Wait for the API call to resolve
    await waitFor(() => {
      expect(api.getDashboard).toHaveBeenCalledTimes(1);
    });

    // Check that the financial values are displayed correctly
    expect(screen.getByText('€24,563.00')).toBeInTheDocument();
    expect(screen.getByText('€8,350.00')).toBeInTheDocument();
    expect(screen.getByText('€5,240.00')).toBeInTheDocument();
    expect(screen.getByText('37.2%')).toBeInTheDocument();
  });

  test('handles API error gracefully', async () => {
    // Mock API error
    api.getDashboard.mockRejectedValue(new Error('Failed to fetch dashboard data'));

    render(
      <ThemeProvider>
        <LanguageProvider>
          <Dashboard />
        </LanguageProvider>
      </ThemeProvider>
    );

    // Wait for the API call to resolve
    await waitFor(() => {
      expect(api.getDashboard).toHaveBeenCalledTimes(1);
    });

    // The component should still render without crashing
    expect(screen.getByText('totalBalance')).toBeInTheDocument();
  });
}); 