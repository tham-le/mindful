import React from 'react';

const BudgetChart = ({ data }) => {
  const { total, spent, remaining } = data;
  const percentSpent = Math.round((spent / total) * 100);
  
  // SVG parameters
  const size = 200;
  const strokeWidth = 30;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  
  // Calculate stroke-dasharray and stroke-dashoffset for the spent portion
  const spentOffset = circumference - (percentSpent / 100) * circumference;
  
  return (
    <div className="flex flex-col items-center justify-center h-full">
      <div className="relative">
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="transparent"
            stroke="#2d3748" // dark background
            strokeWidth={strokeWidth}
          />
          
          {/* Spent portion */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="transparent"
            stroke="#00b8a9" // primary color
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={spentOffset}
            strokeLinecap="round"
          />
        </svg>
        
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <p className="text-3xl font-bold text-white">{percentSpent}%</p>
          <p className="text-sm text-gray-400">of budget used</p>
        </div>
      </div>
      
      <div className="mt-6 grid grid-cols-2 gap-8 w-full max-w-xs">
        <div className="text-center">
          <p className="text-sm text-gray-400">Spent</p>
          <p className="text-xl font-semibold text-white">€{spent}</p>
          <div className="mt-2 h-1 bg-primary rounded-full"></div>
        </div>
        
        <div className="text-center">
          <p className="text-sm text-gray-400">Remaining</p>
          <p className="text-xl font-semibold text-white">€{remaining}</p>
          <div className="mt-2 h-1 bg-dark rounded-full"></div>
        </div>
      </div>
    </div>
  );
};

export default BudgetChart; 