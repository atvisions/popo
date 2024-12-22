/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js,vue}",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        indigo: {
          50: 'rgba(248, 80, 114, 0.1)',   // 最浅色
          100: 'rgba(248, 80, 114, 0.2)',
          200: 'rgba(248, 80, 114, 0.3)',
          300: 'rgba(248, 80, 114, 0.4)',
          400: 'rgba(248, 80, 114, 0.6)',
          500: '#F85072',                   // 基础色
          600: '#000000',  //'#F85072',                   // 常用主色
          700: '#E6405F',                   // 深色
          800: '#D93B58',
          900: '#CC3652',
          950: '#BF3149',                   // 最深色
        },
        primary: {
          DEFAULT: '#F85072',
          dark: '#F63960',
          light: '#FFF1F3',
          lighter: '#FFE4E9',
        }
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}