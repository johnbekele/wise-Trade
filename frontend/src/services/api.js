import axios from 'axios';

const API_BASE_URL = '/api';

// Stock API
export const stockAPI = {
  getQuote: async (symbol) => {
    const response = await axios.get(`${API_BASE_URL}/stocks/quote/${symbol}`);
    return response.data;
  },
  
  getIntraday: async (symbol, interval = '5min') => {
    const response = await axios.get(`${API_BASE_URL}/stocks/intraday/${symbol}`, {
      params: { interval }
    });
    return response.data;
  },
  
  getDaily: async (symbol) => {
    const response = await axios.get(`${API_BASE_URL}/stocks/daily/${symbol}`);
    return response.data;
  },
  
  searchSymbol: async (keywords) => {
    const response = await axios.get(`${API_BASE_URL}/stocks/search`, {
      params: { keywords }
    });
    return response.data;
  },
  
  getOverview: async (symbol) => {
    const response = await axios.get(`${API_BASE_URL}/stocks/overview/${symbol}`);
    return response.data;
  },
  
  getMarketMovers: async () => {
    const response = await axios.get(`${API_BASE_URL}/stocks/market-movers`);
    return response.data;
  },
  
  getMarketStatus: async () => {
    const response = await axios.get(`${API_BASE_URL}/stocks/market-status`);
    return response.data;
  },
  
  getBatchQuotes: async (symbols) => {
    const response = await axios.post(`${API_BASE_URL}/stocks/quotes/batch`, symbols);
    return response.data;
  }
};

// AI News API
export const newsAPI = {
  analyzeNews: async (query) => {
    const response = await axios.get(`${API_BASE_URL}/ai/analyze-news`, {
      params: { query }
    });
    return response.data;
  },
  
  getMarketImpact: async (limit = 10) => {
    const response = await axios.get(`${API_BASE_URL}/ai/market-impact`, {
      params: { limit }
    });
    return response.data;
  }
};

export default {
  stockAPI,
  newsAPI
};

