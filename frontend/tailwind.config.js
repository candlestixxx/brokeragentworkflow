/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'brand-neutral': {
          DEFAULT: '#F8FAFC', // slate-50
          dark: '#0F172A',    // slate-900
        },
        'brand-calm': {
          DEFAULT: '#1D4ED8', // blue-700
          dark: '#3B82F6',    // blue-500
        },
        'brand-accent': {
          DEFAULT: '#38BDF8', // sky-400
          dark: '#7DD3FC',    // sky-300
        }
      },
      fontFamily: {
        'sans': ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'],
      }
    },
  },
  plugins: [],
}
