/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Manrope", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      colors: {
        brand: {
          50: "#f0f4ff",
          100: "#dce6ff",
          200: "#b9ccff",
          300: "#85a6ff",
          400: "#4d76ff",
          500: "#1a4aff",
          600: "#0030e6",
          700: "#0027b8",
          800: "#002096",
          900: "#001a7a",
        },
        slate: {
          950: "#0a0e1a",
        },
      },
    },
  },
  plugins: [],
};
