import React from 'react';

const TestLayout = () => {
  return (
    <div className="min-h-screen bg-gray-900 flex flex-col">
      <nav className="bg-dark-lighter border-b border-dark-border px-4 py-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center">
            <h1 className="text-white text-xl font-bold">Test Layout</h1>
          </div>
        </div>
      </nav>
      
      <div className="flex-1 flex overflow-hidden">
        <div className="flex-1 bg-dark overflow-y-auto p-6">
          <div className="max-w-3xl mx-auto">
            <h1 className="text-2xl font-bold text-white mb-6">Test Content</h1>
            <p className="text-white">If you can see this, the layout is working correctly.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TestLayout; 