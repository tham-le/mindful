import React from 'react';

const ImpulsePurchaseList = ({ purchases }) => {
  // Sort purchases by date (most recent first)
  const sortedPurchases = [...purchases].sort((a, b) => 
    new Date(b.date) - new Date(a.date)
  );
  
  return (
    <div className="h-full flex flex-col">
      <div className="flex-1 overflow-y-auto">
        {sortedPurchases.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-400">No impulse purchase decisions yet</p>
          </div>
        ) : (
          <ul className="space-y-3">
            {sortedPurchases.map((purchase) => (
              <li 
                key={purchase.id} 
                className="bg-dark rounded-lg p-3 flex justify-between items-center"
              >
                <div>
                  <div className="flex items-center">
                    <div 
                      className={`w-2 h-2 rounded-full mr-2 ${
                        purchase.saved ? 'bg-green-500' : 'bg-red-500'
                      }`}
                    ></div>
                    <h4 className="text-white font-medium">{purchase.item}</h4>
                  </div>
                  <p className="text-xs text-gray-400 mt-1">
                    {new Date(purchase.date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric'
                    })}
                  </p>
                </div>
                
                <div className="text-right">
                  <p className={`font-semibold ${purchase.saved ? 'text-green-500' : 'text-red-500'}`}>
                    {purchase.saved ? '+' : '-'}€{purchase.amount}
                  </p>
                  <p className="text-xs text-gray-400 mt-1">
                    {purchase.saved ? 'Saved' : 'Spent'}
                  </p>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-700">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-400">Total Saved</p>
            <p className="text-lg font-semibold text-green-500">
              €{purchases.filter(p => p.saved).reduce((sum, p) => sum + p.amount, 0)}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-400">Total Spent</p>
            <p className="text-lg font-semibold text-red-500">
              €{purchases.filter(p => !p.saved).reduce((sum, p) => sum + p.amount, 0)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImpulsePurchaseList; 