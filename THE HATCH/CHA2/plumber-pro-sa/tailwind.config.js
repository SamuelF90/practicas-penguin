/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'azul-pro': '#0F172A', // Un azul oscuro profesional
        'acento-pro': '#3B82F6', // Azul brillante para botones
      },
    },
  },
  plugins: [],
}