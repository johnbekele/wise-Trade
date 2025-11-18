import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { stockAPI } from '../services/api';
import StockChart from '../components/StockChart';
import { ArrowLeft, RefreshCw } from 'lucide-react';

export default function StockDetail() {
  const { symbol } = useParams();
  const navigate = useNavigate();
  const [quote, setQuote] = useState(null);
  const [overview, setOverview] = useState(null);
  const [intradayData, setIntradayData] = useState(null);
  const [interval, setInterval] = useState('5min');
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [quoteData, overviewData, intradayData] = await Promise.all([
        stockAPI.getQuote(symbol),
        stockAPI.getOverview(symbol).catch(() => null),
        stockAPI.getIntraday(symbol, interval)
      ]);
      
      setQuote(quoteData);
      setOverview(overviewData);
      setIntradayData(intradayData);
    } catch (error) {
      console.error('Error fetching stock detail:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (symbol) {
      fetchData();
    }
  }, [symbol, interval]);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-500">Loading stock details...</p>
      </div>
    );
  }

  const quoteData = quote?.data?.['Global Quote'] || {};
  const price = parseFloat(quoteData['05. price'] || 0);
  const change = parseFloat(quoteData['09. change'] || 0);
  const changePercent = quoteData['10. change percent'] || '0%';
  const isPositive = change >= 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/')}
          className="btn btn-secondary flex items-center gap-2"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Dashboard
        </button>
        <button
          onClick={fetchData}
          className="btn btn-primary flex items-center gap-2"
        >
          <RefreshCw className="w-5 h-5" />
          Refresh
        </button>
      </div>

      {/* Stock Header */}
      <div className="card">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{symbol}</h1>
            {overview?.data?.Name && (
              <p className="text-gray-500 mt-1">{overview.data.Name}</p>
            )}
          </div>
          <div className={`flex items-center gap-2 px-4 py-2 rounded-full text-lg font-medium
            ${isPositive ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}
          >
            {isPositive ? '+' : ''}{change.toFixed(2)} ({changePercent})
          </div>
        </div>
        
        <div className="flex items-end gap-4 mb-6">
          <div className="text-5xl font-bold text-gray-900">${price.toFixed(2)}</div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-gray-200">
          <div>
            <p className="text-gray-500 text-sm">Open</p>
            <p className="font-semibold text-lg">${parseFloat(quoteData['02. open'] || 0).toFixed(2)}</p>
          </div>
          <div>
            <p className="text-gray-500 text-sm">High</p>
            <p className="font-semibold text-lg">${parseFloat(quoteData['03. high'] || 0).toFixed(2)}</p>
          </div>
          <div>
            <p className="text-gray-500 text-sm">Low</p>
            <p className="font-semibold text-lg">${parseFloat(quoteData['04. low'] || 0).toFixed(2)}</p>
          </div>
          <div>
            <p className="text-gray-500 text-sm">Volume</p>
            <p className="font-semibold text-lg">{parseInt(quoteData['06. volume'] || 0).toLocaleString()}</p>
          </div>
        </div>
      </div>

      {/* Chart Controls */}
      <div className="card">
        <div className="flex items-center gap-2 mb-4">
          <span className="font-medium text-gray-700">Interval:</span>
          {['1min', '5min', '15min', '30min', '60min'].map((int) => (
            <button
              key={int}
              onClick={() => setInterval(int)}
              className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors
                ${interval === int 
                  ? 'bg-primary-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
            >
              {int}
            </button>
          ))}
        </div>
        {intradayData && <StockChart data={intradayData} interval={interval} />}
      </div>

      {/* Company Overview */}
      {overview?.data && (
        <div className="card">
          <h2 className="text-2xl font-bold mb-4">Company Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Sector</h3>
              <p className="text-gray-600">{overview.data.Sector || 'N/A'}</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Industry</h3>
              <p className="text-gray-600">{overview.data.Industry || 'N/A'}</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Market Cap</h3>
              <p className="text-gray-600">{overview.data.MarketCapitalization ? 
                `$${(parseInt(overview.data.MarketCapitalization) / 1e9).toFixed(2)}B` : 'N/A'}</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">P/E Ratio</h3>
              <p className="text-gray-600">{overview.data.PERatio || 'N/A'}</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">52 Week High</h3>
              <p className="text-gray-600">${overview.data['52WeekHigh'] || 'N/A'}</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">52 Week Low</h3>
              <p className="text-gray-600">${overview.data['52WeekLow'] || 'N/A'}</p>
            </div>
          </div>
          {overview.data.Description && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-2">Description</h3>
              <p className="text-gray-600 leading-relaxed">{overview.data.Description}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

