/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Albert Sans', 'Inter', 'Geist', 'SF Pro Display', 'system-ui', 'sans-serif'],
        'neo': ['Albert Sans', 'Inter', 'system-ui', 'sans-serif'],
        'inter': ['Inter', 'system-ui', '-apple-system', 'SF Pro Text', 'Segoe UI', 'Roboto', 'Arial', 'sans-serif'],
      },
      letterSpacing: {
        'tight': '-0.025em',
        'tighter': '-0.05em',
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem', letterSpacing: '-0.025em' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem', letterSpacing: '-0.025em' }],
        'base': ['0.9375rem', { lineHeight: '1.5rem', letterSpacing: '-0.025em' }], // 15px
        'lg': ['1.125rem', { lineHeight: '1.75rem', letterSpacing: '-0.025em' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem', letterSpacing: '-0.025em' }],
        '2xl': ['1.5rem', { lineHeight: '2rem', letterSpacing: '-0.025em' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem', letterSpacing: '-0.025em' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem', letterSpacing: '-0.025em' }],
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'slide-down': 'slideDown 0.5s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'slide-up-delay': 'slideUp 0.5s ease-out 0.1s both',
        'slide-up-delay-2': 'slideUp 0.5s ease-out 0.2s both',
        'slide-up-delay-3': 'slideUp 0.5s ease-out 0.3s both',
        'bounce-slow': 'bounce 2s infinite',
        'pulse-slow': 'pulse 3s infinite',
        'wiggle': 'wiggle 1s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        wiggle: {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
      colors: {
        brand: {
          50: '#f0f9f6',
          100: '#d9f0e9',
          200: '#b3e1d3',
          300: '#8dd2bd',
          400: '#67c3a7',
          500: '#4A7C59', // Softer main brand color
          600: '#3f6a4b',
          700: '#34583d',
          800: '#29462f',
          900: '#1e3421',
        },
        mint: {
          50: '#f7fdfb',
          100: '#eefbf8',
          200: '#ddf7f1',
          300: '#ccefea',
          400: '#CFE9E3', // Main mint color
          500: '#b8e0d8',
          600: '#a3d7cd',
          700: '#8ecec2',
          800: '#79c5b7',
          900: '#64bcac',
        },
        sand: {
          50: '#fdfcfb',
          100: '#fbf9f7',
          200: '#f7f3ef',
          300: '#f5f0ea',
          400: '#F3EDE4', // Main sand color
          500: '#f0e8dd',
          600: '#ede2d6',
          700: '#eadccf',
          800: '#e7d6c8',
          900: '#e4d0c1',
        },
        coral: {
          50: '#fef9f7',
          100: '#fdf3f0',
          200: '#fbe7e1',
          300: '#f9dbd2',
          400: '#F8C7B4', // Main coral color
          500: '#f6b3a6',
          600: '#f49f98',
          700: '#f28b8a',
          800: '#f0777c',
          900: '#ee636e',
        },
        primary: {
          50: '#f0f9f6',
          100: '#d9f0e9',
          200: '#b3e1d3',
          300: '#8dd2bd',
          400: '#67c3a7',
          500: '#4A7C59', // Softer brand green
          600: '#3f6a4b',
          700: '#34583d',
          800: '#29462f',
          900: '#1e3421',
        },
        success: {
          50: '#f0f9f6',
          100: '#d9f0e9',
          200: '#b3e1d3',
          300: '#8dd2bd',
          400: '#67c3a7',
          500: '#4A7C59',
          600: '#3f6a4b',
          700: '#34583d',
          800: '#29462f',
          900: '#1e3421',
        },
        warning: {
          50: '#fef9f7',
          100: '#fdf3f0',
          200: '#fbe7e1',
          300: '#f9dbd2',
          400: '#F8C7B4',
          500: '#f6b3a6',
          600: '#f49f98',
          700: '#f28b8a',
          800: '#f0777c',
          900: '#ee636e',
        },
        danger: {
          50: '#fef9f7',
          100: '#fdf3f0',
          200: '#fbe7e1',
          300: '#f9dbd2',
          400: '#F8C7B4',
          500: '#f6b3a6',
          600: '#f49f98',
          700: '#f28b8a',
          800: '#f0777c',
          900: '#ee636e',
        }
      }
    },
  },
  plugins: [],
} 