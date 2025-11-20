# React Query Implementation

This frontend uses **@tanstack/react-query** for efficient data fetching, caching, and state management.

## 📁 Project Structure

```
frontend/src/
├── config/
│   └── config.js              # API base URL configuration
├── hooks/
│   ├── useStocks.js           # Stock-related React Query hooks
│   └── useNews.js             # News-related React Query hooks
├── pages/
│   ├── Dashboard.jsx          # Dashboard with watchlist & market movers
│   ├── StockDetail.jsx        # Individual stock details with charts
│   └── NewsAnalysis.jsx       # AI-powered news analysis
├── components/
│   ├── Layout.jsx             # Main layout wrapper
│   ├── StockCard.jsx          # Stock display card
│   └── StockSearch.jsx        # Stock search component
├── utils/
│   └── helpers.js             # Utility functions (logos, etc.)
└── App.jsx                    # Main app with QueryClientProvider
```

## 🎯 Custom Hooks

### Stock Hooks (`useStocks.js`)

- **`useStockQuote(symbol)`** - Get real-time quote for a single stock
- **`useWatchlist(symbols)`** - Fetch multiple stock quotes (watchlist)
- **`useIntradayData(symbol, interval)`** - Get intraday price data for charts
- **`useStockOverview(symbol)`** - Get company overview and fundamentals
- **`useMarketMovers()`** - Get top gainers, losers, and most active
- **`useStockSearch(keywords)`** - Search for stocks by symbol/name
- **`useStockDetail(symbol, interval)`** - Combined hook for stock detail page

### News Hooks (`useNews.js`)

- **`useMarketImpactNews(limit)`** - Get AI-analyzed market-impacting news
- **`useNewsAnalysis()`** - Mutation hook for custom news analysis
- **`useCachedNewsAnalysis(query)`** - Get cached news analysis results

## ⚙️ React Query Configuration

```javascript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,      // 5 minutes fresh time
      gcTime: 1000 * 60 * 30,        // 30 minutes garbage collection
      refetchOnWindowFocus: false,   // Don't refetch on window focus
      retry: 1,                      // Retry failed requests once
    },
  },
})
```

## 🔄 Cache Strategy

| Data Type | Stale Time | Refetch Interval | Notes |
|-----------|------------|------------------|-------|
| Stock Quote | 30s | 30s | Real-time prices |
| Watchlist | 30s | 30s | Multiple stocks |
| Intraday Data | 1min | Manual | Chart data |
| Stock Overview | 5min | Manual | Company info |
| Market Movers | 1min | 1min | Top gainers/losers |
| Market News | 5min | 5min | AI-analyzed news |
| Stock Search | 5min | Manual | Search results |

## 🚀 Features

### ✅ Automatic Caching
- Query results are automatically cached by React Query
- Background refetching keeps data fresh
- Intelligent cache invalidation

### ✅ Loading & Error States
- Built-in loading and error handling
- Optimistic updates
- Retry logic for failed requests

### ✅ Performance Optimizations
- Request deduplication
- Background refetching
- Garbage collection of unused data
- Automatic stale-while-revalidate

### ✅ Developer Tools
- React Query Devtools included (only in development)
- Visual query inspection
- Cache explorer
- Timeline of queries

## 📊 Example Usage

### In Components

```javascript
import { useStockQuote } from '../hooks/useStocks';

function StockPrice({ symbol }) {
  const { data, isLoading, isError, refetch } = useStockQuote(symbol);
  
  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error loading stock</div>;
  
  return (
    <div>
      <p>Price: ${data.price}</p>
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}
```

### Mutations

```javascript
import { useNewsAnalysis } from '../hooks/useNews';

function NewsAnalyzer() {
  const { analyze, data, isLoading } = useNewsAnalysis();
  
  const handleAnalyze = () => {
    analyze('Tesla earnings');
  };
  
  return (
    <div>
      <button onClick={handleAnalyze} disabled={isLoading}>
        Analyze
      </button>
      {data && <div>{data.analysis}</div>}
    </div>
  );
}
```

## 🔧 Customization

To modify caching behavior for specific hooks, update the hook definition:

```javascript
export function useStockQuote(symbol) {
  return useQuery({
    queryKey: ['stockQuote', symbol],
    queryFn: () => fetchStockQuote(symbol),
    staleTime: 30000,        // Modify this
    refetchInterval: 30000,  // Modify this
    enabled: !!symbol,       // Conditional fetching
  });
}
```

## 🐛 Debugging

### Open React Query Devtools
The devtools are available in development mode at the bottom-left corner of the screen.

### Check Cache State
```javascript
import { useQueryClient } from '@tanstack/react-query';

const queryClient = useQueryClient();
console.log(queryClient.getQueryCache());
```

### Manual Cache Invalidation
```javascript
queryClient.invalidateQueries({ queryKey: ['stockQuote'] });
```

## 📚 Resources

- [React Query Docs](https://tanstack.com/query/latest/docs/react/overview)
- [Query Keys Guide](https://tanstack.com/query/latest/docs/react/guides/query-keys)
- [Mutations Guide](https://tanstack.com/query/latest/docs/react/guides/mutations)

