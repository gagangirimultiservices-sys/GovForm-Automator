/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        govblue: {
          50: "#eef4fb",
          100: "#d7e6f6",
          200: "#aecdee",
          300: "#7fb0e2",
          400: "#4d8fd2",
          500: "#2f72b8",
          600: "#1f5a99",
          700: "#19497d",
          800: "#173e67",
          900: "#163457",
        },
        govgold: {
          400: "#d9a441",
          500: "#c2901f",
        },
      },
      fontFamily: {
        sans: ["Inter", "Segoe UI", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
