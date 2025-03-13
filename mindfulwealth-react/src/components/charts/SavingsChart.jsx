import React from 'react';

const SavingsChart = ({ data, goal }) => {
  // Find the maximum value to scale the chart
  const maxValue = Math.max(...data.map(item => item.amount), goal);
  
  return (
    <div className="h-full flex flex-col">
      {/* Goal line */}
      <div className="flex justify-between items-center mb-2">
        <span className="text-xs text-gray-400">Goal: €{goal}</span>
        <div className="flex items-center">
          <div className="w-3 h-0.5 bg-yellow-500 mr-2"></div>
          <span className="text-xs text-gray-400">Monthly Goal</span>
        </div>
      </div>
      
      <div className="flex-1 flex items-end">
        {data.map((item, index) => (
          <div key={index} className="flex-1 flex flex-col items-center">
            {/* Bar */}
            <div className="relative w-full px-1">
              {/* Goal line */}
              <div 
                className="absolute w-full h-0.5 bg-yellow-500 opacity-70" 
                style={{ 
                  bottom: `${(goal / maxValue) * 100}%`,
                  zIndex: 1
                }}
              ></div>
              
              {/* Bar */}
              <div 
                className="w-full bg-primary rounded-t-sm" 
                style={{ 
                  height: `${(item.amount / maxValue) * 100}%`,
                  minHeight: '4px'
                }}
              ></div>
            </div>
            
            {/* Label */}
            <div className="mt-2 text-xs text-gray-400">{item.month}</div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-gray-400">Average Savings</p>
          <p className="text-lg font-semibold text-white">
            €{Math.round(data.reduce((sum, item) => sum + item.amount, 0) / data.length)}
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-400">Goal Progress</p>
          <p className="text-lg font-semibold text-white">
            {Math.round((data[data.length - 1].amount / goal) * 100)}%
          </p>
        </div>
      </div>
    </div>
  );
};

export default SavingsChart; 