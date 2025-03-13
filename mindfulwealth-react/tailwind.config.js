/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#00b8a9',
          dark: '#00a599',
          light: '#00d6c6',
        },
        dark: {
          DEFAULT: '#1e1e1e',
          lighter: '#252525',
          light: '#2a2a2a',
          border: '#333',
        },
        light: {
          DEFAULT: '#f8fafc',
          darker: '#e2e8f0',
          dark: '#cbd5e1',
          border: '#94a3b8',
        }
      },
      animation: {
        'bounce-slow': 'bounce 1.5s infinite ease-in-out',
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'fade-left': 'fadeLeft 0.3s ease-in-out',
        'fade-right': 'fadeRight 0.3s ease-in-out',
        'scale-in': 'scaleIn 0.3s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        fadeLeft: {
          '0%': { opacity: 0, transform: 'translateX(10px)' },
          '100%': { opacity: 1, transform: 'translateX(0)' },
        },
        fadeRight: {
          '0%': { opacity: 0, transform: 'translateX(-10px)' },
          '100%': { opacity: 1, transform: 'translateX(0)' },
        },
        scaleIn: {
          '0%': { opacity: 0, transform: 'scale(0.9)' },
          '100%': { opacity: 1, transform: 'scale(1)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
} 