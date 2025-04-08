/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./main.py"], 
  safelist: [
    "bg-blue-600",
    "hover:bg-blue-700",
    "text-white",
    "bg-gray-300",
    "text-gray-500",
    "cursor-not-allowed"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
