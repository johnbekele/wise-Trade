import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ArrowLeft, TrendingUp, TrendingDown, RefreshCw, Activity } from 'lucide-react';
import { useStockDetail } from '../hooks/useStocks';
import { getLogoProps } from '../utils/helpers';

export default function StockDetail() {
  const { symbol } = useParams();
  const navigate = useNavigate();
  const [interval, setInterval] = useState('5min');

  // Use React Query hook
  const {
    quote,
    intraday,
    overview,
    isLoading,
    isError,
    error,
    refetch
  } = useStockDetail(symbol, interval);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-500 text-lg">Loading {symbol} data...</p>
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="card bg-red-50 border-red-200 text-center py-12 max-w-2xl mx-auto mt-8">
        <h2 className="text-2xl font-bold text-red-800 mb-4">Error Loading Stock</h2>
        <p className="text-red-600 mb-6">{error?.message || 'Failed to load stock data'}</p>
        <div className="flex gap-4 justify-center">
          <button onClick={() => navigate(-1)} className="btn btn-secondary">
            <ArrowLeft className="w-5 h-5 mr-2" />
            Go Back
          </button>
          <button onClick={refetch} className="btn btn-primary">
            <RefreshCw className="w-5 h-5 mr-2" />
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const quoteData = quote?.data?.['Global Quote'] || {};
  const price = parseFloat(quoteData['05. price'] || 0);
  const change = parseFloat(quoteData['09. change'] || 0);
  const changePercent = quoteData['10. change percent'] || '0%';
  const isPositive = change >= 0;

  // Parse intraday data for chart
  const timeSeries = intraday?.data?.['Time Series (5min)'] || intraday?.data?.['Time Series (15min)'] || {};
  const chartData = Object.entries(timeSeries)
    .slice(0, 50)
    .reverse()
    .map(([time, data]) => ({
      time: new Date(time).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
      price: parseFloat(data['4. close']),
      volume: parseInt(data['5. volume']),
    }));

  const overviewData = overview?.data || {};

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate(-1)}
          className="btn btn-secondary flex items-center gap-2"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>
        <button
          onClick={refetch}
          disabled={isLoading}
          className="btn btn-primary flex items-center gap-2"
        >
          <RefreshCw className={`w-5 h-5 ${isLoading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Stock Header */}
      <div className="card">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-xl bg-gray-100 flex items-center justify-center overflow-hidden border-2 border-gray-200">
              <img 
                {...getLogoProps(symbol)}
                className="w-full h-full object-contain p-2"
              />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{symbol}</h1>
              <p className="text-gray-500">{overviewData.Name || quoteData['01. symbol']}</p>
            </div>
          </div>
          <div className={`flex items-center gap-2 px-4 py-2 rounded-full text-lg font-medium
            ${isPositive ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}
          >
            {isPositive ? <TrendingUp className="w-5 h-5" /> : <TrendingDown className="w-5 h-5" />}
            {changePercent}
          </div>
        </div>

        <div className="mt-6 flex items-end justify-between">
          <div>
            <div className="text-4xl font-bold text-gray-900">${price.toFixed(2)}</div>
            <div className={`text-lg font-medium mt-1 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
              {isPositive ? '+' : ''}{change.toFixed(2)} ({changePercent})
            </div>
          </div>
          <div className="text-right text-sm text-gray-500">
            <div>Last Updated</div>
            <div className="font-medium">{quoteData['07. latest trading day']}</div>
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900">Intraday Chart</h2>
          <div className="flex gap-2">
            {['5min', '15min', '30min', '60min'].map((int) => (
              <button
                key={int}
                onClick={() => setInterval(int)}
                className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors
                  ${interval === int 
                    ? 'bg-primary-600 text-white' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
              >
                {int}
              </button>
            ))}
          </div>
        </div>
        
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="time" 
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                domain={['auto', 'auto']}
                tickFormatter={(value) => `$${value.toFixed(2)}`}
              />
              <Tooltip 
                formatter={(value) => [`$${value.toFixed(2)}`, 'Price']}
                labelFormatter={(label) => `Time: ${label}`}
              />
              <Line 
                type="monotone" 
                dataKey="price" 
                stroke="#3b82f6" 
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="text-center py-12 text-gray-500">
            No intraday data available
          </div>
        )}
      </div>

      {/* Stock Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Key Stats */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5 text-primary-600" />
            Key Statistics
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between py-2 border-b border-gray-200">
              <span className="text-gray-500">Open</span>
              <span className="font-medium">${parseFloat(quoteData['02. open'] || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between py-2 border-b border-gray-200">
              <span className="text-gray-500">High</span>
              <span className="font-medium">${parseFloat(quoteData['03. high'] || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between py-2 border-b border-gray-200">
              <span className="text-gray-500">Low</span>
              <span className="font-medium">${parseFloat(quoteData['04. low'] || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between py-2 border-b border-gray-200">
              <span className="text-gray-500">Previous Close</span>
              <span className="font-medium">${parseFloat(quoteData['08. previous close'] || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-gray-500">Volume</span>
              <span className="font-medium">{parseInt(quoteData['06. volume'] || 0).toLocaleString()}</span>
            </div>
          </div>
        </div>

        {/* Company Info */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Company Information</h3>
          {overviewData.Name ? (
            <div className="space-y-3">
              <div className="flex justify-between py-2 border-b border-gray-200">
                <span className="text-gray-500">Sector</span>
                <span className="font-medium">{overviewData.Sector || 'N/A'}</span>
              </div>
              <div className="flex justify-between py-2 border-b border-gray-200">
                <span className="text-gray-500">Industry</span>
                <span className="font-medium">{overviewData.Industry || 'N/A'}</span>
              </div>
              <div className="flex justify-between py-2 border-b border-gray-200">
                <span className="text-gray-500">Market Cap</span>
                <span className="font-medium">{overviewData.MarketCapitalization ? `$${(parseInt(overviewData.MarketCapitalization) / 1e9).toFixed(2)}B` : 'N/A'}</span>
              </div>
              <div className="flex justify-between py-2 border-b border-gray-200">
                <span className="text-gray-500">P/E Ratio</span>
                <span className="font-medium">{parseFloat(overviewData.PERatio || 0).toFixed(2)}</span>
              </div>
              <div className="flex justify-between py-2">
                <span className="text-gray-500">52 Week High</span>
                <span className="font-medium">${parseFloat(overviewData['52WeekHigh'] || 0).toFixed(2)}</span>
              </div>
            </div>
          ) : (
            <p className="text-gray-500 py-8 text-center">Company information not available</p>
          )}
        </div>
      </div>

      {/* Description */}
      {overviewData.Description && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">About {symbol}</h3>
          <p className="text-gray-600 leading-relaxed">{overviewData.Description}</p>
        </div>
      )}
    </div>
  );
}
