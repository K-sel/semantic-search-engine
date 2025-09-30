import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from "@tailwindcss/vite";


export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    host: '0.0.0.0',  // Permet l'accès depuis l'extérieur du conteneur
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://backend:5000',  // Nom du service dans docker-compose
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')  // Enlève /api du chemin
      }
    }
  }
})