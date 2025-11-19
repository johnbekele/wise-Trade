import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { API_BASE_URL } from '../config/config';

// News API calls
const fetchMarketImpactNews = async (limit = 10) => {
  const response = await axios.get(`${API_BASE_URL}/ai/market-impact`, {
    params: { limit }
  });
  return response.data;
};

const analyzeNews = async (query) => {
  const response = await axios.get(`${API_BASE_URL}/ai/analyze-news`, {
    params: { query }
  });
  return response.data;
};

// Custom hook for market impact news
export function useMarketImpactNews(limit = 10, options = {}) {
  return useQuery({
    queryKey: ['marketImpactNews', limit],
    queryFn: () => fetchMarketImpactNews(limit),
    staleTime: 300000, // 5 minutes
    refetchInterval: 300000, // Auto-refetch every 5 minutes
    ...options, // Allow passing enabled and other options
  });
}

// Custom hook for news analysis mutation
export function useNewsAnalysis() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: analyzeNews,
    onSuccess: (data, variables) => {
      // Cache the result
      queryClient.setQueryData(['newsAnalysis', variables], data);
    },
  });

  return {
    analyze: mutation.mutate,
    analyzeAsync: mutation.mutateAsync,
    data: mutation.data,
    isLoading: mutation.isPending,
    isError: mutation.isError,
    error: mutation.error,
    reset: mutation.reset,
  };
}

// Custom hook to get cached news analysis
export function useCachedNewsAnalysis(query) {
  return useQuery({
    queryKey: ['newsAnalysis', query],
    queryFn: () => analyzeNews(query),
    enabled: false, // Don't auto-fetch, only use cache or manual trigger
    staleTime: 600000, // 10 minutes
  });
}

