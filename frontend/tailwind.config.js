/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'frontier-green': '#00a862',
        'frontier-dark': '#003831',
      }
    },
  },
  plugins: [],
}
