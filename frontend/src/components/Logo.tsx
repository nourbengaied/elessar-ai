import React from 'react';

interface LogoProps {
  size?: number;
  className?: string;
  showText?: boolean;
  variant?: 'default' | 'chip' | 'minimal' | 'pill';
}

const Logo: React.FC<LogoProps> = ({ 
  size = 40, 
  className = '', 
  showText = false, 
  variant = 'default' 
}) => {
  const iconSize = variant === 'chip' ? Math.min(size * 0.7, 28) : size;
  
  const renderIcon = () => (
    <svg 
      width={iconSize} 
      height={iconSize} 
      viewBox="0 0 84 84" 
      aria-label="Dashboard logo"
      className="block transition-transform duration-300 hover:scale-110"
    >
      {/* Brace (parse) - thicker strokes for presence */}
      <path 
        d="M28 14c-8 6 -8 17 0 23c-8 6 -8 17 0 23" 
        fill="none" 
        stroke="#0C1D16" 
        strokeWidth="8" 
        strokeLinecap="round"
        className="transition-all duration-300"
      />
      {/* Wave (sea) - enhanced positioning and thickness with green color */}
      <path 
        d="M40 48c 8 0 10 -10 18 -10c 7 0 10 5 12 10" 
        fill="none" 
        stroke="#2F6F5E" 
        strokeWidth="9" 
        strokeLinecap="round"
        className="transition-all duration-300 animate-float"
      />
    </svg>
  );

  const renderText = () => (
    <span className="font-inter font-semibold tracking-tight text-lg leading-none text-[#0C1D16] transition-all duration-300 hover:scale-105">
      Dash<span className="bg-gradient-to-r from-[#2F6F5E] to-[#14B78F] bg-clip-text text-transparent">board</span>
    </span>
  );

  if (variant === 'pill') {
    return (
      <div className={`flex items-center gap-1 ${className} group`}>
        <div 
          className="rounded-full bg-gradient-to-r from-[#2F6F5E] to-[#14B78F] p-2 shadow-[0_4px_12px_rgba(47,111,94,0.3)] transition-all duration-300 hover:shadow-[0_8px_25px_rgba(47,111,94,0.4)] hover:scale-105"
          style={{ 
            width: `${size + 16}px`, 
            height: `${size + 16}px`,
            borderRadius: `${(size + 16) / 2}px`
          }}
        >
          <div className="w-full h-full bg-white rounded-full flex items-center justify-center shadow-inner transition-all duration-300 group-hover:shadow-lg">
            {renderIcon()}
          </div>
        </div>
        {showText && renderText()}
      </div>
    );
  }

  if (variant === 'chip') {
    return (
      <div className={`flex items-center gap-1 ${className} group`}>
        <div 
          className="rounded-full bg-[#EAF4EF] border border-[rgba(12,29,22,0.08)] shadow-[0_1px_2px_rgba(0,0,0,0.04),0_6px_16px_rgba(0,0,0,0.06)] grid place-items-center transition-all duration-300 hover:shadow-[0_4px_20px_rgba(0,0,0,0.1)] hover:scale-105 hover:border-[rgba(12,29,22,0.15)]"
          style={{ width: `${size}px`, height: `${size}px` }}
        >
          {renderIcon()}
        </div>
        {showText && renderText()}
      </div>
    );
  }

  if (variant === 'minimal') {
    return (
      <div className={`flex items-center gap-1 ${className} group`}>
        {renderIcon()}
        {showText && renderText()}
      </div>
    );
  }

  // Default variant
  return (
    <div className={`flex items-center gap-1 ${className} group`}>
      {renderIcon()}
      {showText && renderText()}
    </div>
  );
};

export default Logo; 