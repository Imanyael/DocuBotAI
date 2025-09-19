/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#3b82f6',
          dark: '#1e40af',
        },
        secondary: {
          DEFAULT: '#334155',
          dark: '#0f172a',
        },
        accent: '#06b6d4',
        success: '#059669',
        warning: '#d97706',
        error: '#dc2626',
        dark: '#0f172a',
        light: '#f8fafc',
        neutral: {
          DEFAULT: '#94a3b8',
          dark: '#64748b',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      backdropFilter: {
        'glass': 'blur(10px)',
      },
      borderRadius: {
        DEFAULT: '8px',
        lg: '12px',
      },
      animation: {
        'hover-lift': 'hover-lift 0.3s ease-out',
      },
      keyframes: {
        'hover-lift': {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(-2px)' },
        },
      },
    },
  },
  plugins: [],
}