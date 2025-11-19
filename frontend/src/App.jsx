import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { AuthProvider } from './context/AuthContext'
import Dashboard from './pages/Dashboard'
import StockDetail from './pages/StockDetail'
import NewsAnalysis from './pages/NewsAnalysis'
import Login from './pages/Login'
import Signup from './pages/Signup'
import EmailVerification from './pages/EmailVerification'
import Layout from './components/Layout'

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // Data is considered fresh for 5 minutes
      gcTime: 1000 * 60 * 30, // Garbage collection time (was cacheTime)
      refetchOnWindowFocus: false, // Don't refetch when window regains focus
      retry: 1, // Retry failed requests once
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <Routes>
            {/* Auth routes without layout */}
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/verify-email" element={<EmailVerification />} />
            
            {/* App routes with layout */}
            <Route path="/" element={<Layout><Dashboard /></Layout>} />
            <Route path="/stock/:symbol" element={<Layout><StockDetail /></Layout>} />
            <Route path="/news" element={<Layout><NewsAnalysis /></Layout>} />
          </Routes>
        </Router>
        {/* React Query Devtools - only in development */}
        <ReactQueryDevtools initialIsOpen={false} />
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App

