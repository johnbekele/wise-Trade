import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import StockCard from '../components/StockCard';
import StockSearch from '../components/StockSearch';
import { stockAPI } from '../services/api';
import { TrendingUp, TrendingDown, Activity, RefreshCw } from 'lucide-react';

export default function Dashboard() {
  const navigate = useNavigate();
  const [watchlist, setWatchlist] = useState(['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']);
  const [stockData, setStockData] = useState({});
  const [marketMovers, setMarketMovers] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchStockData = async () => {
    setLoading(true);
    try {
      const promises = watchlist.map(symbol => 
        stockAPI.getQuote(symbol).catch(err => ({ symbol, error: err.message }))
      );
      const results = await Promise.all(promises);
      
      const dataMap = {};
      results.forEach((result, index) => {
        if (!result.error) {
          dataMap[watchlist[index]] = result;
        }
      });
      
      setStockData(dataMap);
    } catch (error) {
      console.error('Error fetching stock data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMarketMovers = async () => {
    try {
      const data = await stockAPI.getMarketMovers();
      setMarketMovers(data);
    } catch (error) {
      console.error('Error fetching market movers:', error);
    }
  };

  useEffect(() => {
    fetchStockData();
    fetchMarketMovers();
    
    // Refresh data every 30 seconds
    const interval = setInterval(() => {
      setRefreshing(true);
      fetchStockData().finally(() => setRefreshing(false));
    }, 30000);
    
    return () => clearInterval(interval);
  }, [watchlist]);

  const handleAddStock = (symbol) => {
    if (!watchlist.includes(symbol)) {
      setWatchlist([...watchlist, symbol]);
    }
  };

  const handleRemoveStock = (symbol) => {
    setWatchlist(watchlist.filter(s => s !== symbol));
  };

  const handleRefresh = () => {
    setRefreshing(true);
    Promise.all([fetchStockData(), fetchMarketMovers()])
      .finally(() => setRefreshing(false));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Trading Dashboard</h1>
          <p className="text-gray-500 mt-1">Real-time stock market information</p>
        </div>
        <button 
          onClick={handleRefresh}
          disabled={refreshing}
          className="btn btn-primary flex items-center gap-2"
        >
          <RefreshCw className={`w-5 h-5 ${refreshing ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Search Bar */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Add Stock to Watchlist</h2>
        <StockSearch onSelect={handleAddStock} />
      </div>

      {/* Market Movers */}
      {marketMovers && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="card bg-gradient-to-br from-green-50 to-white">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Top Gainers</h3>
            </div>
            <div className="space-y-2">
              {marketMovers.top_gainers?.slice(0, 3).map((stock, index) => (
                <div key={index} className="flex justify-between items-center text-sm">
                  <span className="font-medium">{stock.ticker}</span>
                  <span className="text-green-600 font-medium">
                    +{parseFloat(stock.change_percentage).toFixed(2)}%
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="card bg-gradient-to-br from-red-50 to-white">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-red-100 rounded-lg">
                <TrendingDown className="w-6 h-6 text-red-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Top Losers</h3>
            </div>
            <div className="space-y-2">
              {marketMovers.top_losers?.slice(0, 3).map((stock, index) => (
                <div key={index} className="flex justify-between items-center text-sm">
                  <span className="font-medium">{stock.ticker}</span>
                  <span className="text-red-600 font-medium">
                    {parseFloat(stock.change_percentage).toFixed(2)}%
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="card bg-gradient-to-br from-blue-50 to-white">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Activity className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Most Active</h3>
            </div>
            <div className="space-y-2">
              {marketMovers.most_actively_traded?.slice(0, 3).map((stock, index) => (
                <div key={index} className="flex justify-between items-center text-sm">
                  <span className="font-medium">{stock.ticker}</span>
                  <span className="text-gray-600 text-xs">
                    Vol: {parseInt(stock.volume).toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Watchlist */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Your Watchlist</h2>
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-500">Loading stocks...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {watchlist.map((symbol) => (
              <div key={symbol} className="relative">
                <button
                  onClick={() => handleRemoveStock(symbol)}
                  className="absolute top-2 right-2 z-10 p-1 bg-red-100 text-red-600 rounded-full hover:bg-red-200 transition-colors"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
                <StockCard
                  symbol={symbol}
                  data={stockData[symbol]}
                  onClick={() => navigate(`/stock/${symbol}`)}
                />
              </div>
            ))}
          </div>
        )}
        
        {watchlist.length === 0 && !loading && (
          <div className="card text-center py-12">
            <p className="text-gray-500">No stocks in watchlist. Add some using the search above!</p>
          </div>
        )}
      </div>
    </div>
  );
}

