import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App.tsx'
import '@fontsource/inter/400.css'
import '@fontsource/inter/500.css'
import '@fontsource/inter/600.css'
import '@fontsource/inter/700.css'
import './index.css'

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000, // Data is fresh for 1 second
      retry: (failureCount, error) => {
        // Don't retry if it's a network error and we're on first attempt
        if (failureCount === 0 && error instanceof Error && error.message.includes('fetch')) {
          console.log('🔗 Trying to connect to SimuLife API...');
        }
        return failureCount < 3; // Retry up to 3 times
      },
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000), // Exponential backoff
    },
  },
})

createRoot(document.getElementById("root")!).render(
  <QueryClientProvider client={queryClient}>
    <App />
  </QueryClientProvider>
);
