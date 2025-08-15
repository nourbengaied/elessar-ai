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
      colors: {
        brand: {
          50: '#f0f9f6',
          100: '#d9f0e9',
          200: '#b3e1d3',
          300: '#8dd2bd',
          400: '#67c3a7',
          500: '#2F6F5E', // Main brand color
          600: '#2a5f51',
          700: '#254f44',
          800: '#203f37',
          900: '#1b2f2a',
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
          500: '#2F6F5E', // Brand green
          600: '#2a5f51',
          700: '#254f44',
          800: '#203f37',
          900: '#1b2f2a',
        },
        success: {
          50: '#f0f9f6',
          100: '#d9f0e9',
          200: '#b3e1d3',
          300: '#8dd2bd',
          400: '#67c3a7',
          500: '#2F6F5E',
          600: '#2a5f51',
          700: '#254f44',
          800: '#203f37',
          900: '#1b2f2a',
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