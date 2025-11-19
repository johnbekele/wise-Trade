import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { API_BASE_URL } from '../config/config';

// Stock API calls
const fetchStockQuote = async (symbol) => {
  const response = await axios.get(`${API_BASE_URL}/stocks/quote/${symbol}`);
  return response.data;
};

const fetchMultipleQuotes = async (symbols) => {
  const promises = symbols.map(symbol => 
    fetchStockQuote(symbol).catch(err => ({ symbol, error: err.message }))
  );
  return Promise.all(promises);
};

const fetchIntraday = async ({ symbol, interval }) => {
  // Map interval to backend format and use /candles endpoint
  const response = await axios.get(`${API_BASE_URL}/stocks/candles/${symbol}`, {
    params: { resolution: interval, days: 7 }
  });
  return response.data;
};

const fetchStockOverview = async (symbol) => {
  // Use /profile endpoint instead of /overview
  const response = await axios.get(`${API_BASE_URL}/stocks/profile/${symbol}`);
  return response.data;
};

const fetchMarketMovers = async () => {
  const response = await axios.get(`${API_BASE_URL}/stocks/market-movers`);
  return response.data;
};

const searchStocks = async (keywords) => {
  const response = await axios.get(`${API_BASE_URL}/stocks/search`, {
    params: { keywords }
  });
  return response.data;
};

// Custom hook for single stock quote
export function useStockQuote(symbol) {
  return useQuery({
    queryKey: ['stockQuote', symbol],
    queryFn: () => fetchStockQuote(symbol),
    enabled: !!symbol,
    staleTime: 30000, // 30 seconds
    refetchInterval: 30000, // Auto-refetch every 30 seconds
  });
}

// Custom hook for multiple stock quotes (watchlist)
export function useWatchlist(symbols) {
  return useQuery({
    queryKey: ['watchlist', symbols],
    queryFn: () => fetchMultipleQuotes(symbols),
    enabled: symbols.length > 0,
    staleTime: 30000,
    refetchInterval: 30000,
  });
}

// Custom hook for intraday data
export function useIntradayData(symbol, interval = '5min') {
  return useQuery({
    queryKey: ['intraday', symbol, interval],
    queryFn: () => fetchIntraday({ symbol, interval }),
    enabled: !!symbol,
    staleTime: 60000, // 1 minute
  });
}

// Custom hook for stock overview
export function useStockOverview(symbol) {
  return useQuery({
    queryKey: ['stockOverview', symbol],
    queryFn: () => fetchStockOverview(symbol),
    enabled: !!symbol,
    staleTime: 300000, // 5 minutes
  });
}

// Custom hook for market movers
export function useMarketMovers() {
  return useQuery({
    queryKey: ['marketMovers'],
    queryFn: fetchMarketMovers,
    staleTime: 60000, // 1 minute
    refetchInterval: 60000,
  });
}

// Custom hook for stock search
export function useStockSearch(keywords) {
  return useQuery({
    queryKey: ['stockSearch', keywords],
    queryFn: () => searchStocks(keywords),
    enabled: keywords.length >= 2,
    staleTime: 300000, // 5 minutes
  });
}

// Custom hook for stock detail page (combines quote, intraday, overview)
export function useStockDetail(symbol, interval = '5min') {
  const quote = useStockQuote(symbol);
  const intraday = useIntradayData(symbol, interval);
  const overview = useStockOverview(symbol);

  return {
    quote: quote.data,
    intraday: intraday.data,
    overview: overview.data,
    isLoading: quote.isLoading || intraday.isLoading || overview.isLoading,
    isError: quote.isError || intraday.isError || overview.isError,
    error: quote.error || intraday.error || overview.error,
    refetch: () => {
      quote.refetch();
      intraday.refetch();
      overview.refetch();
    }
  };
}

