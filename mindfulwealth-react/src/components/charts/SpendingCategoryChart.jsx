import React from 'react';

const SpendingCategoryChart = ({ categories }) => {
  // Calculate total spent
  const totalSpent = categories.reduce((sum, category) => sum + category.amount, 0);
  
  // Calculate total budget
  const totalBudget = categories.reduce((sum, category) => sum + category.budget, 0);
  
  return (
    <div className="h-full flex flex-col">
      <div className="flex-1 overflow-y-auto">
        {categories.map((category, index) => {
          const percentOfTotal = totalSpent > 0 ? Math.round((category.amount / totalSpent) * 100) : 0;
          const percentOfBudget = category.budget > 0 ? Math.round((category.amount / category.budget) * 100) : 0;
          
          return (
            <div key={index} className="mb-4">
              <div className="flex justify-between items-center mb-1">
                <div className="flex items-center">
                  <div 
                    className="w-3 h-3 rounded-full mr-2" 
                    style={{ backgroundColor: category.color }}
                  ></div>
                  <span className="text-sm text-white">{category.name}</span>
                </div>
                <div className="text-right">
                  <span className="text-sm text-white">€{category.amount}</span>
                  <span className="text-xs text-gray-400 ml-1">/ €{category.budget}</span>
                </div>
              </div>
              
              {/* Progress bar */}
              <div className="h-2 bg-dark rounded-full overflow-hidden">
                <div 
                  className="h-full rounded-full" 
                  style={{ 
                    width: `${percentOfBudget}%`,
                    backgroundColor: category.color,
                    opacity: percentOfBudget > 100 ? '0.8' : '1'
                  }}
                ></div>
              </div>
              
              {/* Percentage */}
              <div className="flex justify-between mt-1">
                <span className="text-xs text-gray-400">{percentOfBudget}% of budget</span>
                <span className="text-xs text-gray-400">{percentOfTotal}% of total</span>
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-700">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-400">Total Spent</span>
          <span className="text-lg font-semibold text-white">€{totalSpent}</span>
        </div>
        <div className="flex justify-between items-center mt-1">
          <span className="text-sm text-gray-400">Total Budget</span>
          <span className="text-sm text-gray-400">€{totalBudget}</span>
        </div>
      </div>
    </div>
  );
};

export default SpendingCategoryChart; 