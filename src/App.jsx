import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import StockDetail from './pages/StockDetail'
import NewsAnalysis from './pages/NewsAnalysis'
import Layout from './components/Layout'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/stock/:symbol" element={<StockDetail />} />
          <Route path="/news" element={<NewsAnalysis />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

