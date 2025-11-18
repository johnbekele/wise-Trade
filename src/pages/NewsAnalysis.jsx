import { useState, useEffect } from 'react';
import { newsAPI } from '../services/api';
import { Newspaper, TrendingUp, RefreshCw } from 'lucide-react';

export default function NewsAnalysis() {
  const [analysis, setAnalysis] = useState('');
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [marketImpactNews, setMarketImpactNews] = useState('');
  const [loadingMarket, setLoadingMarket] = useState(true);

  const fetchMarketImpact = async () => {
    setLoadingMarket(true);
    try {
      const data = await newsAPI.getMarketImpact(10);
      setMarketImpactNews(data.analysis);
    } catch (error) {
      console.error('Error fetching market impact:', error);
      setMarketImpactNews('Error loading market impact news');
    } finally {
      setLoadingMarket(false);
    }
  };

  useEffect(() => {
    fetchMarketImpact();
  }, []);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const data = await newsAPI.analyzeNews(query);
      setAnalysis(data.analysis);
    } catch (error) {
      console.error('Error analyzing news:', error);
      setAnalysis('Error analyzing news. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">AI News Analysis</h1>
        <p className="text-gray-500 mt-1">AI-powered market news analysis and insights</p>
      </div>

      {/* Market Impact News */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-primary-600" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Top Market-Impact News</h2>
              <p className="text-sm text-gray-500">AI-analyzed news that could affect markets</p>
            </div>
          </div>
          <button
            onClick={fetchMarketImpact}
            disabled={loadingMarket}
            className="btn btn-secondary flex items-center gap-2"
          >
            <RefreshCw className={`w-5 h-5 ${loadingMarket ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {loadingMarket ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-500">Analyzing market news...</p>
          </div>
        ) : (
          <div className="prose max-w-none">
            <div className="bg-gray-50 rounded-lg p-6 whitespace-pre-wrap">
              {marketImpactNews}
            </div>
          </div>
        )}
      </div>

      {/* Custom News Analysis */}
      <div className="card">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Newspaper className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Analyze Specific News</h2>
            <p className="text-sm text-gray-500">Search for news about a company or topic</p>
          </div>
        </div>

        <form onSubmit={handleAnalyze} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Enter company name or topic
            </label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., Tesla, Federal Reserve, tech stocks..."
              className="input"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="btn btn-primary w-full md:w-auto"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <RefreshCw className="w-5 h-5 animate-spin" />
                Analyzing...
              </span>
            ) : (
              'Analyze News'
            )}
          </button>
        </form>

        {analysis && (
          <div className="mt-6 pt-6 border-t border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-4">Analysis Results</h3>
            <div className="prose max-w-none">
              <div className="bg-blue-50 rounded-lg p-6 whitespace-pre-wrap">
                {analysis}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Tips */}
      <div className="card bg-gradient-to-br from-amber-50 to-white border-amber-200">
        <h3 className="font-semibold text-gray-900 mb-3">💡 Tips for Better Analysis</h3>
        <ul className="space-y-2 text-sm text-gray-700">
          <li className="flex items-start gap-2">
            <span className="text-amber-600 mt-0.5">•</span>
            <span>Be specific with company names or topics (e.g., "Apple earnings" instead of just "Apple")</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-amber-600 mt-0.5">•</span>
            <span>The AI analyzes recent news articles and provides market impact insights</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-amber-600 mt-0.5">•</span>
            <span>Market impact news is updated regularly to show breaking developments</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-amber-600 mt-0.5">•</span>
            <span>Use insights as a starting point for your own research - not as sole trading advice</span>
          </li>
        </ul>
      </div>
    </div>
  );
}

