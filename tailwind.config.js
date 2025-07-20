/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./app/**/*.py"
  ],
  theme: {
    screens: {
      // Custom breakpoints for Success-Diary
      'xs': '375px',   // iPhone SE and small mobile devices
      'md': '768px',   // Tablets and large mobile devices  
      'lg': '1024px',  // Desktop and laptops
      'xl': '1440px',  // Large desktop screens
    },
    extend: {
      // Future custom styling extensions can go here
    },
  },
  plugins: [],
}

