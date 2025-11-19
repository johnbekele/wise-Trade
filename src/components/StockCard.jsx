import { TrendingUp, TrendingDown } from 'lucide-react';
import { Link } from 'react-router-dom';
import { getLogoProps } from '../utils/helpers';

export default function StockCard({ symbol, data, onClick }) {
  const quote = data?.data?.['Global Quote'] || {};
  const price = parseFloat(quote['05. price'] || 0);
  const change = parseFloat(quote['09. change'] || 0);
  const changePercent = quote['10. change percent'] || '0%';
  const isPositive = change >= 0;

  return (
    <div 
      onClick={onClick}
      className="card hover:shadow-lg transition-shadow cursor-pointer"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {/* Company Logo */}
          <div className="w-12 h-12 rounded-lg bg-gray-100 flex items-center justify-center overflow-hidden border border-gray-200">
            <img 
              {...getLogoProps(symbol)}
              className="w-full h-full object-contain p-1"
            />
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-900">{symbol}</h3>
            <p className="text-sm text-gray-500">{quote['01. symbol']}</p>
          </div>
        </div>
        <div className={`flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium
          ${isPositive ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}
        >
          {isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
          {changePercent}
        </div>
      </div>
      
      <div className="space-y-2">
        <div className="flex justify-between items-end">
          <span className="text-3xl font-bold">${price.toFixed(2)}</span>
          <span className={`text-lg font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
            {isPositive ? '+' : ''}{change.toFixed(2)}
          </span>
        </div>
        
        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200 text-sm">
          <div>
            <p className="text-gray-500">High</p>
            <p className="font-medium">${parseFloat(quote['03. high'] || 0).toFixed(2)}</p>
          </div>
          <div>
            <p className="text-gray-500">Low</p>
            <p className="font-medium">${parseFloat(quote['04. low'] || 0).toFixed(2)}</p>
          </div>
          <div>
            <p className="text-gray-500">Volume</p>
            <p className="font-medium">{parseInt(quote['06. volume'] || 0).toLocaleString()}</p>
          </div>
          <div>
            <p className="text-gray-500">Prev Close</p>
            <p className="font-medium">${parseFloat(quote['08. previous close'] || 0).toFixed(2)}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

