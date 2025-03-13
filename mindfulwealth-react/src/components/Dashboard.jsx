import React, { useState, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  BarElement,
  ArcElement,
  Title, 
  Tooltip, 
  Legend,
  Filler
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  BarElement,
  ArcElement,
  Title, 
  Tooltip, 
  Legend,
  Filler
);

const Dashboard = () => {
  const { t } = useLanguage();
  const { layoutStyle } = useTheme();
  const [tipOfTheDay, setTipOfTheDay] = useState('');
  
  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);
  
  // Mock data - in a real app, this would come from an API
  const mockData = {
    monthlyExpenses: [1200, 1350, 1100, 1450, 1300, 1200],
    monthlyIncome: [2500, 2500, 2700, 2500, 2500, 3000],
    savingsRate: [0.25, 0.23, 0.28, 0.21, 0.24, 0.30],
    expenseCategories: {
      housing: 35,
      food: 15,
      transportation: 10,
      entertainment: 15,
      utilities: 10,
      other: 15
    }
  };
  
  const tips = [
    t('tip1'),
    t('tip2'),
    t('tip3'),
    t('tip4'),
    t('tip5')
  ];
  
  useEffect(() => {
    // Set a random tip of the day
    const randomTip = tips[Math.floor(Math.random() * tips.length)];
    setTipOfTheDay(randomTip);
  }, [tips]);
  
  // Last 6 months labels
  const getLastSixMonths = () => {
    const months = [];
    const date = new Date();
    
    for (let i = 5; i >= 0; i--) {
      const month = new Date(date.getFullYear(), date.getMonth() - i, 1);
      months.push(month.toLocaleString('default', { month: 'short' }));
    }
    
    return months;
  };
  
  const months = getLastSixMonths();
  
  // Chart data
  const incomeVsExpensesData = {
    labels: months,
    datasets: [
      {
        label: t('income'),
        data: mockData.monthlyIncome,
        borderColor: layoutStyle === 'modern' ? '#7ECBEA' : 'rgba(75, 192, 192, 1)',
        backgroundColor: layoutStyle === 'modern' 
          ? 'rgba(168, 216, 234, 0.4)' 
          : 'rgba(75, 192, 192, 0.2)',
        fill: true,
        tension: 0.4,
        borderWidth: layoutStyle === 'modern' ? 3 : 2
      },
      {
        label: t('expenses'),
        data: mockData.monthlyExpenses,
        borderColor: layoutStyle === 'modern' ? '#F9AFAF' : 'rgba(255, 99, 132, 1)',
        backgroundColor: layoutStyle === 'modern' 
          ? 'rgba(249, 175, 175, 0.4)' 
          : 'rgba(255, 99, 132, 0.2)',
        fill: true,
        tension: 0.4,
        borderWidth: layoutStyle === 'modern' ? 3 : 2
      }
    ]
  };
  
  const savingsRateData = {
    labels: months,
    datasets: [
      {
        label: t('savingsRate'),
        data: mockData.savingsRate.map(rate => rate * 100),
        backgroundColor: layoutStyle === 'modern' 
          ? [
              'rgba(168, 216, 234, 0.8)',
              'rgba(249, 175, 175, 0.8)',
              'rgba(246, 213, 92, 0.8)',
              'rgba(185, 251, 192, 0.8)',
              'rgba(255, 225, 86, 0.8)',
              'rgba(126, 203, 234, 0.8)'
            ]
          : 'rgba(153, 102, 255, 0.6)',
        borderColor: layoutStyle === 'modern'
          ? [
              'rgba(168, 216, 234, 1)',
              'rgba(249, 175, 175, 1)',
              'rgba(246, 213, 92, 1)',
              'rgba(185, 251, 192, 1)',
              'rgba(255, 225, 86, 1)',
              'rgba(126, 203, 234, 1)'
            ]
          : 'rgba(153, 102, 255, 1)',
        borderWidth: layoutStyle === 'modern' ? 2 : 1,
        borderRadius: layoutStyle === 'modern' ? 4 : 0,
        hoverOffset: 4
      }
    ]
  };
  
  const expenseCategoriesData = {
    labels: [
      t('housing'),
      t('food'),
      t('transportation'),
      t('entertainment'),
      t('utilities'),
      t('other')
    ],
    datasets: [
      {
        data: Object.values(mockData.expenseCategories),
        backgroundColor: layoutStyle === 'modern' 
          ? [
              'rgba(168, 216, 234, 0.8)', // Light blue
              'rgba(249, 175, 175, 0.8)', // Light pink
              'rgba(246, 213, 92, 0.8)',  // Yellow
              'rgba(185, 251, 192, 0.8)', // Light green
              'rgba(255, 225, 86, 0.8)',  // Light yellow
              'rgba(126, 203, 234, 0.8)'  // Darker blue
            ]
          : [
              'rgba(255, 99, 132, 0.8)',   // Red
              'rgba(54, 162, 235, 0.8)',   // Blue
              'rgba(255, 206, 86, 0.8)',   // Yellow
              'rgba(75, 192, 192, 0.8)',   // Green
              'rgba(153, 102, 255, 0.8)',  // Purple
              'rgba(255, 159, 64, 0.8)'    // Orange
            ],
        borderWidth: 2,
        borderColor: layoutStyle === 'modern'
          ? [
              'rgba(168, 216, 234, 1)', // Light blue
              'rgba(249, 175, 175, 1)', // Light pink
              'rgba(246, 213, 92, 1)',  // Yellow
              'rgba(185, 251, 192, 1)', // Light green
              'rgba(255, 225, 86, 1)',  // Light yellow
              'rgba(126, 203, 234, 1)'  // Darker blue
            ]
          : 'rgba(30, 41, 59, 0.8)',
        hoverOffset: 15
      }
    ]
  };
  
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: 'var(--color-text-primary)',
          font: {
            weight: 'bold',
            size: 12
          },
          padding: 20,
          usePointStyle: layoutStyle === 'modern',
          pointStyle: 'circle',
          boxWidth: layoutStyle === 'modern' ? 10 : 40,
          boxHeight: layoutStyle === 'modern' ? 10 : 12
        }
      },
      tooltip: {
        backgroundColor: layoutStyle === 'modern' ? 'rgba(168, 216, 234, 0.9)' : 'rgba(0, 0, 0, 0.7)',
        titleFont: {
          size: 14,
          weight: 'bold'
        },
        bodyFont: {
          size: 13
        },
        padding: 12,
        cornerRadius: 8,
        displayColors: true,
        borderColor: layoutStyle === 'modern' ? 'rgba(255, 255, 255, 0.3)' : 'transparent',
        borderWidth: layoutStyle === 'modern' ? 1 : 0,
        boxShadow: layoutStyle === 'modern' ? '0 4px 6px rgba(0, 0, 0, 0.1)' : 'none'
      }
    },
    scales: {
      x: {
        grid: {
          color: layoutStyle === 'modern' 
            ? 'rgba(255, 255, 255, 0.1)' 
            : 'var(--color-border)'
        },
        ticks: {
          color: 'var(--color-text-primary)',
          font: {
            weight: 'bold',
            size: 11
          },
          padding: 8
        }
      },
      y: {
        grid: {
          color: layoutStyle === 'modern' 
            ? 'rgba(255, 255, 255, 0.1)' 
            : 'var(--color-border)'
        },
        ticks: {
          color: 'var(--color-text-primary)',
          font: {
            weight: 'bold',
            size: 11
          },
          padding: 8
        }
      }
    },
    elements: {
      point: {
        radius: layoutStyle === 'modern' ? 4 : 3,
        hoverRadius: layoutStyle === 'modern' ? 6 : 5,
        backgroundColor: layoutStyle === 'modern' ? 'white' : undefined,
        borderWidth: layoutStyle === 'modern' ? 2 : 1
      },
      line: {
        tension: 0.4
      }
    }
  };
  
  const barChartOptions = {
    ...chartOptions,
    plugins: {
      ...chartOptions.plugins,
      tooltip: {
        ...chartOptions.plugins.tooltip,
        callbacks: {
          label: function(context) {
            return context.dataset.label + ': ' + context.raw + '%';
          }
        }
      }
    }
  };
  
  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        display: false,
        labels: {
          color: 'var(--color-text-primary)',
          font: {
            weight: 'bold',
            size: 12
          },
          padding: 20,
          usePointStyle: true,
          pointStyle: 'circle',
          boxWidth: 10,
          boxHeight: 10
        }
      },
      tooltip: {
        backgroundColor: layoutStyle === 'modern' ? 'rgba(168, 216, 234, 0.9)' : 'rgba(0, 0, 0, 0.7)',
        titleFont: {
          size: 14,
          weight: 'bold'
        },
        bodyFont: {
          size: 13
        },
        padding: 12,
        cornerRadius: 8,
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.raw || 0;
            const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
            const percentage = Math.round((value / total) * 100);
            return `${label}: €${value} (${percentage}%)`;
          }
        }
      }
    },
    cutout: '60%',
    borderWidth: 2,
    borderColor: layoutStyle === 'modern' ? 'rgba(255, 255, 255, 0.8)' : 'rgba(30, 41, 59, 0.8)'
  };
  
  return (
    <div className="flex-1 overflow-y-auto p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">
          {layoutStyle === 'modern' && <span className="emoji-chart mr-2"></span>}
          {t('financialDashboard')}
        </h1>
        
        <div className={`${layoutStyle === 'modern' ? 'dashboard-card' : 'glass-card'} p-4 mb-6`}>
          <div className="flex items-center">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${layoutStyle === 'modern' ? 'gradient-accent' : 'bg-primary/20 text-primary'}`}>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <h2 className="text-lg font-semibold">{t('tipOfTheDay')}</h2>
              <p className="opacity-70">{tipOfTheDay}</p>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div className={`${layoutStyle === 'modern' ? 'dashboard-card' : 'glass-card'} p-4`}>
            <h2 className="text-lg font-semibold mb-4">
              {layoutStyle === 'modern' && <span className="emoji-money mr-2"></span>}
              {t('incomeVsExpenses')}
            </h2>
            <div className="h-80 chart-container">
              <Line data={incomeVsExpensesData} options={chartOptions} />
            </div>
          </div>
          
          <div className={`${layoutStyle === 'modern' ? 'dashboard-card' : 'glass-card'} p-4`}>
            <h2 className="text-lg font-semibold mb-4">
              {layoutStyle === 'modern' && <span className="emoji-chart mr-2"></span>}
              {t('savingsRate')}
            </h2>
            <div className="h-80 chart-container">
              <Bar data={savingsRateData} options={barChartOptions} />
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className={`${layoutStyle === 'modern' ? 'dashboard-card' : 'glass-card'} p-4 lg:col-span-1`}>
            <h2 className="text-lg font-semibold mb-4">
              {layoutStyle === 'modern' && <span className="emoji-wallet mr-2"></span>}
              {t('expenseBreakdown')}
            </h2>
            <div className="h-80 chart-container">
              <Doughnut data={expenseCategoriesData} options={doughnutOptions} />
            </div>
            <div className="expense-breakdown-legend">
              {expenseCategoriesData.labels.map((label, index) => (
                <div key={index} className="expense-breakdown-legend-item">
                  <div 
                    className="expense-breakdown-legend-color" 
                    style={{ 
                      backgroundColor: Array.isArray(expenseCategoriesData.datasets[0].backgroundColor) 
                        ? expenseCategoriesData.datasets[0].backgroundColor[index] 
                        : expenseCategoriesData.datasets[0].backgroundColor 
                    }}
                  ></div>
                  <span className="whitespace-nowrap overflow-hidden text-ellipsis">
                    {label}: €{Object.values(mockData.expenseCategories)[index]}
                  </span>
                </div>
              ))}
            </div>
          </div>
          
          <div className={`${layoutStyle === 'modern' ? 'dashboard-card' : 'glass-card'} p-4 lg:col-span-2`}>
            <h2 className="text-lg font-semibold mb-4">
              {layoutStyle === 'modern' && <span className="emoji-money mr-2"></span>}
              {t('financialSummary')}
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className={`p-4 rounded-lg ${layoutStyle === 'modern' ? 'gradient-primary text-white' : ''}`} style={{ 
                backgroundColor: layoutStyle !== 'modern' ? 'var(--color-bg-tertiary)' : 'transparent' 
              }}>
                <div className="text-sm opacity-90 font-medium mb-1">{t('currentMonthIncome')}</div>
                <div className="text-2xl font-bold">€{mockData.monthlyIncome[5].toLocaleString()}</div>
              </div>
              
              <div className={`p-4 rounded-lg ${layoutStyle === 'modern' ? 'gradient-accent text-white' : ''}`} style={{ 
                backgroundColor: layoutStyle !== 'modern' ? 'var(--color-bg-tertiary)' : 'transparent' 
              }}>
                <div className="text-sm opacity-90 font-medium mb-1">{t('currentMonthExpenses')}</div>
                <div className="text-2xl font-bold">€{mockData.monthlyExpenses[5].toLocaleString()}</div>
              </div>
              
              <div className="p-4 rounded-lg" style={{ 
                backgroundColor: layoutStyle === 'modern' ? 'var(--modern-color-bright)' : 'var(--color-bg-tertiary)',
                color: layoutStyle === 'modern' ? 'var(--modern-color-text-on-light)' : 'var(--color-text-primary)',
                boxShadow: layoutStyle === 'modern' ? '0 4px 6px rgba(0, 0, 0, 0.05)' : 'none'
              }}>
                <div className="text-sm opacity-90 font-medium mb-1">{t('currentSavingsRate')}</div>
                <div className="text-2xl font-bold">{(mockData.savingsRate[5] * 100).toFixed(1)}%</div>
              </div>
              
              <div className="p-4 rounded-lg" style={{ 
                backgroundColor: layoutStyle === 'modern' ? 'var(--modern-color-secondary)' : 'var(--color-bg-tertiary)',
                color: layoutStyle === 'modern' ? 'var(--modern-color-text-on-dark)' : 'var(--color-text-primary)',
                boxShadow: layoutStyle === 'modern' ? '0 4px 6px rgba(0, 0, 0, 0.05)' : 'none'
              }}>
                <div className="text-sm opacity-90 font-medium mb-1">{t('biggestExpenseCategory')}</div>
                <div className="text-2xl font-bold">{t('housing')}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 