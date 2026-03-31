/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./index.html",
      "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: 'class', 
    theme: {
      extend: {
        fontFamily: {
          sans: ['"Space Grotesk"', 'sans-serif'],
          display: ['"Inter"', 'sans-serif'],
        },
        colors: {
            brand: {
                dark: '#050B14',
                light: '#F8FAFC',
                pink: '#EC4899',
                teal: '#14B8A6',
                indigo: '#4F46E5',
                blue: '#3B82F6'
            }
        },
        animation: {
            'float': 'float 8s ease-in-out infinite',
            'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        },
        keyframes: {
            float: {
                '0%, 100%': { transform: 'translateY(0) rotate(0deg)' },
                '50%': { transform: 'translateY(-15px) rotate(1deg)' },
            }
        }
      },
    },
    plugins: [],
}
