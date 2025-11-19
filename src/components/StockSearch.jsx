import { Search, X, TrendingUp } from 'lucide-react';
import { useState, useEffect } from 'react';
import { stockAPI } from '../services/api';

export default function StockSearch({ onSelect }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    if (query.length < 2) {
      setResults([]);
      setShowResults(false);
      return;
    }

    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const data = await stockAPI.searchSymbol(query);
        // Handle both old format (bestMatches) and new format (results array)
        const searchResults = data.results || data.quotes || [];
        setResults(searchResults);
        setShowResults(true);
      } catch (error) {
        console.error('Search error:', error);
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [query]);

  const handleSelect = (symbol) => {
    onSelect(symbol);
    setQuery('');
    setShowResults(false);
    setResults([]);
  };

  return (
    <div className="relative">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by company name or symbol (e.g., Apple, AAPL, Tesla)..."
          className="input pl-10 pr-10"
        />
        {query && (
          <button
            onClick={() => {
              setQuery('');
              setResults([]);
              setShowResults(false);
            }}
            className="absolute right-3 top-1/2 transform -translate-y-1/2"
          >
            <X className="w-5 h-5 text-gray-400 hover:text-gray-600" />
          </button>
        )}
      </div>

      {showResults && (
        <div className="absolute z-10 w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-200 max-h-96 overflow-y-auto">
          {loading ? (
            <div className="p-4 text-center text-gray-500">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-2"></div>
              Searching...
            </div>
          ) : results.length > 0 ? (
            <div className="py-2">
              {results.map((result, index) => {
                // Support multiple data formats
                const symbol = result.symbol || result['1. symbol'];
                const name = result.longname || result.shortname || result['2. name'] || symbol;
                const type = result.quoteType || result['3. type'] || 'EQUITY';
                const region = result.exchDisp || result['4. region'] || 'US';
                
                return (
                  <button
                    key={index}
                    onClick={() => handleSelect(symbol)}
                    className="w-full px-4 py-3 hover:bg-blue-50 text-left transition-colors border-b border-gray-100 last:border-0"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <p className="font-bold text-gray-900 text-lg">{symbol}</p>
                          <span className="px-2 py-0.5 text-xs bg-blue-100 text-blue-700 rounded-full">
                            {type}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">{name}</p>
                      </div>
                      <div className="flex items-center gap-2 ml-4">
                        <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">{region}</span>
                        <TrendingUp className="w-4 h-4 text-green-500" />
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          ) : query.length >= 2 ? (
            <div className="p-4 text-center text-gray-500">
              <p className="font-medium">No results found</p>
              <p className="text-sm mt-1">Try searching for: Apple, Tesla, Microsoft, or stock symbols like AAPL, TSLA</p>
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
}

