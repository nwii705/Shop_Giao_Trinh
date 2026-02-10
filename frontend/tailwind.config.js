/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'gemini-bg': '#1a1a2e',
        'gemini-dark': '#1e1e30',
        'gemini-card': '#252540',
        'gemini-sidebar': '#131320',
        'gemini-hover': '#2a2a4a',
        'gemini-border': '#3a3a5a',
        'gemini-blue': '#4285f4',
        'gemini-purple': '#a855f7',
        'gemini-gradient-start': '#4285f4',
        'gemini-gradient-end': '#a855f7',
      },
    },
  },
  plugins: [],
}
