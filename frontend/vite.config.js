import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

// Em dev, as chamadas para /api são repassadas ao backend FastAPI (porta 8000),
// evitando CORS. Em produção o frontend usa VITE_API_URL (ver src/api.js).
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
