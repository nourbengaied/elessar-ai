import React from 'react';

interface LogoProps {
  size?: number;
  className?: string;
  showText?: boolean;
}

const Logo: React.FC<LogoProps> = ({ size = 40, className = '', showText = true }) => {
  return (
    <div className={`flex items-center ${className}`}>
      <svg 
        width={size} 
        height={size} 
        viewBox="0 0 84 84" 
        aria-label="Parsea icon — Sand & Ink"
        className="flex-shrink-0"
      >
        {/* Brace (parse) */}
        <path 
          d="M28 14 c-8 6 -8 17 0 23 c-8 6 -8 17 0 23" 
          fill="none" 
          stroke="#0C1D16" 
          strokeWidth="6" 
          strokeLinecap="round"
        />
        {/* Wave (sea) */}
        <path 
          d="M40 48 c 8 0 10 -8 18 -8 c 7 0 10 4 12 8" 
          fill="none" 
          stroke="#2F6F5E" 
          strokeWidth="7" 
          strokeLinecap="round"
        />
      </svg>
      {showText && (
        <span className="ml-2 text-lg font-bold text-brand-500 tracking-tight font-neo">
          Parsea
        </span>
      )}
    </div>
  );
};

export default Logo; 