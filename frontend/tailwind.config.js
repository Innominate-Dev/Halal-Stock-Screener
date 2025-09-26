/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
      },
      colors: {
        primary: '#2563EB',   // Blue 600
        secondary: '#4F46E5', // Indigo 700
        accent: '#F59E0B',    // Amber 500
        background: '#F3F4F6', // Gray 100
        textPrimary: '#111827', // Gray 900
        textSecondary: '#6B7280', // Gray 500
      },
      borderRadius: {
        'xl': '1rem',
      }
    },
  },
  plugins: [],
}
