import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Export the configuration as a single object
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ['9caae56956ea.ngrok-free.app', 'localhost']
  }
})
