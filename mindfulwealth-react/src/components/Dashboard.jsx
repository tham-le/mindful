import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';
import {
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  ClockIcon,
  ChartBarIcon,
  CurrencyDollarIcon,
  BanknotesIcon
} from '@heroicons/react/24/outline';

const StatCard = ({ title, value, icon, change, changeType }) => {
  return (
    <div className="bg-white dark:bg-dark-300 rounded-lg shadow-sm p-6">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
          <h3 className="text-2xl font-bold mt-1">{value}</h3>
        </div>
        <div className="p-2 bg-primary bg-opacity-10 rounded-lg">
          {icon}
        </div>
      </div>
      {change && (
        <div className="mt-4 flex items-center">
          {changeType === 'up' ? (
            <ArrowTrendingUpIcon className="w-4 h-4 text-green-500 mr-1" />
          ) : (
            <ArrowTrendingDownIcon className="w-4 h-4 text-red-500 mr-1" />
          )}
          <span className={`text-sm ${changeType === 'up' ? 'text-green-500' : 'text-red-500'}`}>
            {change}
          </span>
          <span className="text-sm text-gray-500 dark:text-gray-400 ml-1">vs last month</span>
        </div>
      )}
    </div>
  );
};

const ActivityItem = ({ title, time, amount, type }) => {
  return (
    <div className="flex items-center justify-between py-3 border-b border-gray-200 dark:border-gray-700 last:border-0">
      <div className="flex items-center">
        <div className={`p-2 rounded-full ${type === 'deposit' ? 'bg-green-100 dark:bg-green-900' : 'bg-red-100 dark:bg-red-900'
          }`}>
          {type === 'deposit' ? (
            <ArrowTrendingUpIcon className="w-4 h-4 text-green-500 dark:text-green-400" />
          ) : (
            <ArrowTrendingDownIcon className="w-4 h-4 text-red-500 dark:text-red-400" />
          )}
        </div>
        <div className="ml-3">
          <p className="font-medium">{title}</p>
          <p className="text-sm text-gray-500 dark:text-gray-400 flex items-center">
            <ClockIcon className="w-3 h-3 mr-1" /> {time}
          </p>
        </div>
      </div>
      <div className={`font-medium ${type === 'deposit' ? 'text-green-500 dark:text-green-400' : 'text-red-500 dark:text-red-400'
        }`}>
        {type === 'deposit' ? '+' : '-'}{amount}
      </div>
    </div>
  );
};

const Dashboard = () => {
  const { t } = useLanguage();
  const { theme } = useTheme();

  // Scroll to top when component mounts
  React.useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title={t('totalBalance')}
          value="€24,563.00"
          icon={<BanknotesIcon className="w-6 h-6 text-primary" />}
          change="2.5%"
          changeType="up"
        />
        <StatCard
          title={t('monthlyIncome')}
          value="€8,350.00"
          icon={<ArrowTrendingUpIcon className="w-6 h-6 text-primary" />}
          change="1.8%"
          changeType="up"
        />
        <StatCard
          title={t('monthlyExpenses')}
          value="€5,240.00"
          icon={<ArrowTrendingDownIcon className="w-6 h-6 text-primary" />}
          change="0.5%"
          changeType="down"
        />
        <StatCard
          title={t('savingsRate')}
          value="37.2%"
          icon={<ChartBarIcon className="w-6 h-6 text-primary" />}
          change="3.1%"
          changeType="up"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white dark:bg-dark-300 rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">{t('portfolioOverview')}</h2>
          <div className="h-64 flex items-center justify-center bg-light-300 dark:bg-dark-200 rounded-lg">
            <p className="text-gray-500 dark:text-gray-400">{t('portfolioChartPlaceholder')}</p>
          </div>
          <div className="grid grid-cols-3 gap-4 mt-6">
            <div className="text-center">
              <p className="text-sm text-gray-500 dark:text-gray-400">{t('stocks')}</p>
              <p className="text-lg font-bold mt-1">45%</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-500 dark:text-gray-400">{t('bonds')}</p>
              <p className="text-lg font-bold mt-1">30%</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-500 dark:text-gray-400">{t('cash')}</p>
              <p className="text-lg font-bold mt-1">25%</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-dark-300 rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">{t('recentActivity')}</h2>
          <div className="space-y-0">
            <ActivityItem
              title={t('salaryDeposit')}
              time={t('today')}
              amount="€3,500.00"
              type="deposit"
            />
            <ActivityItem
              title={t('rentPayment')}
              time={t('yesterday')}
              amount="€1,200.00"
              type="withdrawal"
            />
            <ActivityItem
              title={t('investmentReturn')}
              time="Mar 15, 9:45 AM"
              amount="€450.00"
              type="deposit"
            />
            <ActivityItem
              title={t('groceryShopping')}
              time="Mar 14, 6:30 PM"
              amount="€85.75"
              type="withdrawal"
            />
          </div>
          <button className="w-full mt-4 py-2 text-center text-primary hover:text-primary-dark font-medium">
            {t('viewAllTransactions')}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-dark-300 rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">{t('financialGoals')}</h2>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-1">
                <span className="font-medium">{t('emergencyFund')}</span>
                <span>75%</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                <div className="bg-primary h-2.5 rounded-full" style={{ width: '75%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="font-medium">{t('vacationSavings')}</span>
                <span>45%</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                <div className="bg-primary h-2.5 rounded-full" style={{ width: '45%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="font-medium">{t('homeDownPayment')}</span>
                <span>30%</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                <div className="bg-primary h-2.5 rounded-full" style={{ width: '30%' }}></div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-dark-300 rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">{t('financialInsights')}</h2>
          <div className="space-y-4">
            <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <h3 className="font-medium text-green-800 dark:text-green-400">{t('positiveTrend')}</h3>
              <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                {t('positiveTrendDescription')}
              </p>
            </div>
            <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
              <h3 className="font-medium text-yellow-800 dark:text-yellow-400">{t('suggestion')}</h3>
              <p className="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                {t('suggestionDescription')}
              </p>
            </div>
            <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <h3 className="font-medium text-blue-800 dark:text-blue-400">{t('opportunity')}</h3>
              <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                {t('opportunityDescription')}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 