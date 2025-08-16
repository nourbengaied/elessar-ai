import React from 'react';
import Logo from './Logo';

const LogoDemo: React.FC = () => {
  return (
    <div className="p-8 space-y-8 bg-white">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Logo Variants Demo</h1>
      
      {/* Original vs Improved */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-gray-800">Comparison</h2>
        <div className="flex items-center gap-8 p-4 bg-gray-50 rounded-lg">
          <div className="text-center">
            <p className="text-sm text-gray-600 mb-2">Original</p>
            <div className="flex items-center gap-2">
              <svg width="40" height="40" viewBox="0 0 84 84" aria-label="Original Dashboard icon">
                <path d="M28 14 c-8 6 -8 17 0 23 c-8 6 -8 17 0 23" 
                      fill="none" stroke="#0C1D16" strokeWidth="6" strokeLinecap="round"/>
                <path d="M40 48 c 8 0 10 -8 18 -8 c 7 0 10 4 12 8" 
                      fill="none" stroke="#2F6F5E" strokeWidth="7" strokeLinecap="round"/>
              </svg>
              <span className="text-lg font-bold text-[#0C1D16] tracking-tight">Dashboard</span>
            </div>
          </div>
          
          <div className="text-center">
            <p className="text-sm text-gray-600 mb-2">Improved</p>
            <Logo size={40} variant="default" />
          </div>
        </div>
      </div>

      {/* Different Variants */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-gray-800">Logo Variants</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Default</h3>
            <Logo size={48} variant="default" />
          </div>
          
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Chip Style</h3>
            <Logo size={48} variant="chip" />
          </div>
          
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Pill Style</h3>
            <Logo size={48} variant="pill" />
          </div>
          
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Minimal</h3>
            <Logo size={48} variant="minimal" />
          </div>
        </div>
      </div>

      {/* Different Sizes */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-gray-800">Size Variations</h2>
        <div className="flex items-center gap-6 flex-wrap">
          <Logo size={24} variant="pill" />
          <Logo size={32} variant="pill" />
          <Logo size={40} variant="pill" />
          <Logo size={48} variant="pill" />
          <Logo size={56} variant="pill" />
        </div>
      </div>

      {/* Icon Only */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-gray-800">Icon Only</h2>
        <div className="flex items-center gap-6 flex-wrap">
          <Logo size={24} showText={false} variant="pill" />
          <Logo size={32} showText={false} variant="pill" />
          <Logo size={40} showText={false} variant="pill" />
          <Logo size={48} showText={false} variant="pill" />
        </div>
      </div>

      {/* Background Contexts */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-gray-800">Background Contexts</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-6 bg-[#0C1D16] rounded-lg">
            <Logo size={40} variant="pill" className="text-white" />
          </div>
          <div className="p-6 bg-gradient-to-r from-[#2F6F5E] to-[#14B78F] rounded-lg">
            <Logo size={40} variant="pill" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogoDemo; 