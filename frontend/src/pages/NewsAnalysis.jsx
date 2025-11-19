import { useState } from 'react';
import { Newspaper, TrendingUp, RefreshCw, Search, AlertCircle, ArrowUp, ArrowDown, Minus, Building2, Lightbulb, CheckCircle, Target, Zap, Lock, LogIn } from 'lucide-react';
import { useMarketImpactNews, useNewsAnalysis } from '../hooks/useNews';
import { getLogoProps } from '../utils/helpers';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

// Helper function to parse and structure markdown-like analysis text
function parseAnalysisText(text) {
  if (!text) return { sections: [], rawText: '' };

  const lines = text.split('\n');
  const sections = [];
  let currentSection = null;
  let currentItems = [];
  let currentParagraph = [];

  lines.forEach((line, index) => {
    const trimmedLine = line.trim();
    
    // Skip empty lines
    if (!trimmedLine) {
      // If we have accumulated paragraph text, add it to current item
      if (currentParagraph.length > 0 && currentItems.length > 0) {
        const lastItem = currentItems[currentItems.length - 1];
        const paragraphText = currentParagraph.join(' ').trim();
        if (lastItem.description) {
          lastItem.description += ' ' + paragraphText;
        } else {
          lastItem.description = paragraphText;
        }
        currentParagraph = [];
      }
      return;
    }

    // Main section headers (### or numbered section like "2. ")
    if (trimmedLine.match(/^#{1,4}\s+\d+\./) || trimmedLine.match(/^\d+\.\s+[A-Z][^a-z]{10,}/) || trimmedLine.match(/^#{1,4}\s+[A-Z]/)) {
      // Save previous section
      if (currentSection) {
        currentSection.items = currentItems;
        sections.push(currentSection);
      }
      
      currentSection = {
        title: trimmedLine.replace(/^#{1,4}\s+/, '').replace(/^\d+\.\s+/, '').trim(),
        items: [],
        content: []
      };
      currentItems = [];
      currentParagraph = [];
    }
    // Numbered list items with bold (1. **Title**)
    else if (trimmedLine.match(/^\d+\.\s+\*\*/)) {
      // Flush paragraph to previous item
      if (currentParagraph.length > 0 && currentItems.length > 0) {
        const lastItem = currentItems[currentItems.length - 1];
        lastItem.description = (lastItem.description || '') + ' ' + currentParagraph.join(' ').trim();
        currentParagraph = [];
      }

      const match = trimmedLine.match(/^\d+\.\s+\*\*(.+?)\*\*(.*)/) || trimmedLine.match(/^\d+\.\s+(.+)/);
      if (match) {
        currentItems.push({
          type: 'item',
          title: match[1]?.trim() || match[0].replace(/^\d+\.\s+/, '').trim(),
          description: match[2]?.trim() || '',
          subPoints: []
        });
      }
    }
    // Bullet points or sub-items with indentation
    else if (trimmedLine.match(/^\s*[\*\-•]\s+/) || trimmedLine.match(/^\s{2,}[\*\-•]/)) {
      const match = trimmedLine.match(/^\s*[\*\-•]\s+\*\*(.+?)\*\*:?\s*(.*)/) || trimmedLine.match(/^\s*[\*\-•]\s+(.+)/);
      if (match) {
        if (currentItems.length > 0) {
          currentItems[currentItems.length - 1].subPoints.push({
            label: match[1]?.includes(':') ? match[1].replace(':', '').trim() : '',
            text: match[2]?.trim() || match[1]?.trim() || match[0].replace(/^\s*[\*\-•]\s+/, '').trim()
          });
        } else if (currentSection) {
          // Add as section content if no items yet
          currentSection.content.push(trimmedLine);
        }
      }
      currentParagraph = [];
    }
    // Regular paragraph text - accumulate
    else if (trimmedLine && currentSection) {
      currentParagraph.push(trimmedLine);
    }
  });

  // Flush any remaining paragraph
  if (currentParagraph.length > 0 && currentItems.length > 0) {
    const lastItem = currentItems[currentItems.length - 1];
    lastItem.description = (lastItem.description || '') + ' ' + currentParagraph.join(' ').trim();
  }

  // Save last section
  if (currentSection) {
    currentSection.items = currentItems;
    sections.push(currentSection);
  }

  return { sections, rawText: text };
}

export default function NewsAnalysis() {
  const [query, setQuery] = useState('');
  const { isAuthenticated } = useAuth();

  // Only fetch data if user is authenticated
  const {
    data: marketImpactData,
    isLoading: loadingMarket,
    refetch: refetchMarketImpact
  } = useMarketImpactNews(10, { enabled: isAuthenticated });

  const {
    analyze,
    data: analysisData,
    isLoading: loadingAnalysis,
    reset: resetAnalysis
  } = useNewsAnalysis();

  const marketImpactNews = marketImpactData?.news_items || [];

  const handleAnalyze = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    analyze(query);
  };

  const getImpactColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'high': return 'bg-red-500';
      case 'medium': return 'bg-amber-500';
      case 'low': return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  const getImpactDirectionIcon = (direction) => {
    switch (direction?.toLowerCase()) {
      case 'positive': return <ArrowUp className="w-4 h-4 text-green-500" />;
      case 'negative': return <ArrowDown className="w-4 h-4 text-red-500" />;
      case 'neutral': return <Minus className="w-4 h-4 text-gray-500" />;
      default: return null;
    }
  };

  // Parse analysis text when available
  const parsedAnalysis = analysisData ? parseAnalysisText(analysisData.analysis) : null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">AI News Analysis</h1>
        <p className="text-gray-500 mt-1">AI-powered market news analysis and insights</p>
      </div>

      {/* Show login prompt if not authenticated */}
      {!isAuthenticated ? (
        <div className="card bg-gradient-to-br from-blue-50 via-white to-purple-50 border-blue-200">
          <div className="text-center py-16 px-4">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mb-6 shadow-lg">
              <Lock className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-3">
              AI News Analysis Requires Authentication
            </h2>
            <p className="text-gray-600 mb-8 max-w-md mx-auto">
              Sign in to access AI-powered market news analysis, trading insights, and personalized recommendations
            </p>
            
            {/* Features List */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8 max-w-3xl mx-auto">
              <div className="bg-white rounded-lg p-4 border border-blue-200">
                <TrendingUp className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                <h3 className="font-semibold text-gray-900 mb-1">Market Impact Analysis</h3>
                <p className="text-sm text-gray-600">AI-analyzed news affecting markets</p>
              </div>
              <div className="bg-white rounded-lg p-4 border border-purple-200">
                <Search className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                <h3 className="font-semibold text-gray-900 mb-1">Custom Analysis</h3>
                <p className="text-sm text-gray-600">Search and analyze any topic</p>
              </div>
              <div className="bg-white rounded-lg p-4 border border-green-200">
                <Lightbulb className="w-8 h-8 text-green-600 mx-auto mb-2" />
                <h3 className="font-semibold text-gray-900 mb-1">Trading Insights</h3>
                <p className="text-sm text-gray-600">Actionable recommendations</p>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex items-center justify-center gap-4">
              <Link
                to="/login"
                className="inline-flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                <LogIn className="w-5 h-5" />
                Sign In
              </Link>
              <Link
                to="/signup"
                className="inline-flex items-center gap-2 px-8 py-3 bg-white border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium"
              >
                Create Free Account
              </Link>
            </div>

            {/* Additional Info */}
            <div className="mt-8 pt-8 border-t border-blue-200">
              <div className="flex items-center justify-center gap-6 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>100% Free</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>No Credit Card</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Instant Access</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <>
          {/* Market Impact News - Only shown when authenticated */}
          <div className="card bg-gradient-to-br from-green-50 to-white border-green-200">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Top Market-Impact News</h2>
              <p className="text-sm text-gray-500">AI-analyzed news that could affect markets</p>
            </div>
          </div>
          <button
            onClick={() => refetchMarketImpact()}
            disabled={loadingMarket}
            className="btn btn-secondary flex items-center gap-2"
          >
            <RefreshCw className={`w-5 h-5 ${loadingMarket ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {loadingMarket ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mx-auto"></div>
            <p className="mt-4 text-gray-500">Analyzing market news...</p>
          </div>
        ) : marketImpactNews.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {marketImpactNews.map((item, index) => (
              <div key={index} className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow border border-green-100 overflow-hidden">
                <div className="p-5">
                  <div className="flex items-center justify-between mb-3">
                    <span className="flex items-center gap-2 text-sm font-semibold text-green-700">
                      <span className="w-6 h-6 flex items-center justify-center rounded-full bg-green-500 text-white text-xs font-bold">{item.rank}</span>
                      {item.source}
                    </span>
                    <div className="flex items-center gap-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium text-white ${getImpactColor(item.impact_level)}`}>
                        {item.impact_level}
                      </span>
                      {getImpactDirectionIcon(item.impact_direction)}
                    </div>
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 mb-3">{item.title}</h3>

                  {/* Why It Matters */}
                  <div className="mb-4 bg-white rounded-lg p-3 border border-green-100">
                    <p className="text-sm font-semibold text-gray-700 mb-1">💡 Why It Matters:</p>
                    <p className="text-sm text-gray-600 leading-relaxed">{item.why_it_matters}</p>
                  </div>

                  {/* Affected Sectors & Companies */}
                  {(item.affected_sectors?.length > 0 || item.affected_companies?.length > 0) && (
                    <div className="grid grid-cols-2 gap-3 mb-4">
                      {item.affected_sectors?.length > 0 && (
                        <div className="bg-purple-50 rounded-lg p-3 border border-purple-100">
                          <div className="flex items-center gap-1 mb-2">
                            <Building2 className="w-4 h-4 text-purple-600" />
                            <p className="text-xs font-semibold text-purple-700">Sectors:</p>
                          </div>
                          <div className="flex flex-wrap gap-1">
                            {item.affected_sectors.slice(0, 3).map((sector, i) => (
                              <span key={i} className="text-xs px-2 py-0.5 bg-purple-100 text-purple-700 rounded">
                                {sector}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      {item.affected_companies?.length > 0 && (
                        <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
                          <div className="flex items-center gap-1 mb-2">
                            <TrendingUp className="w-4 h-4 text-blue-600" />
                            <p className="text-xs font-semibold text-blue-700">Companies:</p>
                          </div>
                          <div className="flex flex-wrap gap-1">
                            {item.affected_companies.slice(0, 3).map((company, i) => (
                              <div key={i} className="flex items-center gap-1 bg-blue-100 rounded pl-1 pr-2 py-0.5">
                                <img 
                                  {...getLogoProps(company)}
                                  className="w-4 h-4 rounded object-contain"
                                />
                                <span className="text-xs text-blue-700">{company}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Trading Insight */}
                  {item.trading_insight && (
                    <div className="bg-gradient-to-r from-amber-50 to-amber-100 rounded-lg p-3 border border-amber-200">
                      <div className="flex items-start gap-2">
                        <Lightbulb className="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm font-semibold text-amber-800 mb-1">Trading Insight:</p>
                          <p className="text-sm text-amber-700 leading-relaxed">{item.trading_insight}</p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <AlertCircle className="w-12 h-12 text-gray-400 mx-auto" />
            <p className="mt-4 text-gray-500">No market-impacting news found or an error occurred.</p>
          </div>
        )}
      </div>

      {/* Custom News Analysis */}
      <div className="card bg-gradient-to-br from-blue-50 to-white border-blue-200">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-blue-100 rounded-lg">
            <Search className="w-6 h-6 text-blue-600" />
          </div>
          <div className="flex-1">
            <h2 className="text-xl font-bold text-gray-900">Analyze Specific News</h2>
            <p className="text-sm text-gray-600">Get AI-powered insights on any market topic</p>
          </div>
          {!isAuthenticated && (
            <span className="inline-flex items-center gap-2 px-3 py-1.5 bg-yellow-50 text-yellow-700 text-sm font-medium rounded-lg border border-yellow-200">
              <Lock className="w-4 h-4" />
              Login Required
            </span>
          )}
        </div>

        {!isAuthenticated ? (
          <div className="text-center py-12 px-4">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
              <Lock className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Sign in to unlock AI Analysis
            </h3>
            <p className="text-gray-600 mb-6">
              Create a free account to access personalized AI-powered news analysis and trading insights
            </p>
            <div className="flex items-center justify-center gap-4">
              <Link
                to="/login"
                className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                <LogIn className="w-5 h-5" />
                Sign In
              </Link>
              <Link
                to="/signup"
                className="inline-flex items-center gap-2 px-6 py-3 bg-white border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium"
              >
                Create Account
              </Link>
            </div>
          </div>
        ) : (
          <>
            <form onSubmit={handleAnalyze} className="flex flex-col md:flex-row gap-4">
              <div className="flex-grow">
                <label htmlFor="news-query" className="sr-only">
                  Enter company name or topic
                </label>
                <input
                  id="news-query"
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="e.g., Tesla earnings, Federal Reserve policy, tech stocks..."
                  className="input w-full"
                  disabled={loadingAnalysis}
                />
              </div>

              <button
                type="submit"
                disabled={loadingAnalysis || !query.trim()}
                className="btn btn-primary flex items-center justify-center gap-2 px-6 py-2.5"
              >
                {loadingAnalysis ? (
                  <>
                    <RefreshCw className="w-5 h-5 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5" />
                    Analyze News
                  </>
                )}
              </button>
            </form>

        {/* Beautiful Structured Analysis Results */}
        {analysisData && (
          <div className="mt-6 pt-6 border-t border-blue-200">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-xl font-bold text-gray-900">Analysis Results</h3>
                <p className="text-sm text-gray-500">"{analysisData.query}"</p>
              </div>
              <button
                onClick={resetAnalysis}
                className="text-sm px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
              >
                Clear
              </button>
            </div>

            {/* Render formatted text with proper styling */}
            <div className="space-y-4">
              {parsedAnalysis.rawText.split('\n').map((line, idx) => {
                const trimmed = line.trim();
                if (!trimmed) return <div key={idx} className="h-2"></div>;

                // Section headers (### or numbered headers)
                if (trimmed.match(/^#{1,4}\s/) || trimmed.match(/^\d+\.\s+[A-Z][^a-z]{10,}/)) {
                  const text = trimmed.replace(/^#{1,4}\s+/, '').replace(/^\d+\.\s+/, '');
                  const icon = idx < 5 ? [
                    <Target className="w-5 h-5" />,
                    <Building2 className="w-5 h-5" />,
                    <TrendingUp className="w-5 h-5" />,
                    <Lightbulb className="w-5 h-5" />
                  ][Math.min(idx, 3)] : null;
                  
                  return (
                    <div key={idx} className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4 rounded-lg shadow-sm">
                      <h4 className="text-lg font-bold text-white flex items-center gap-2">
                        {icon}
                        {text}
                      </h4>
                    </div>
                  );
                }

                // Numbered items with bold (1. **Title**)
                if (trimmed.match(/^\d+\.\s+\*\*/)) {
                  const match = trimmed.match(/^\d+\.\s+\*\*(.+?)\*\*(.*)/) || trimmed.match(/^\d+\.\s+(.+)/);
                  const title = match[1]?.trim() || '';
                  const description = match[2]?.trim() || '';
                  
                  return (
                    <div key={idx} className="bg-blue-50 border-l-4 border-blue-400 rounded-r-lg p-4 ml-4">
                      <div className="flex gap-3">
                        <div className="flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full bg-blue-500 text-white text-xs font-bold">
                          {trimmed.match(/^(\d+)\./)[1]}
                        </div>
                        <div className="flex-1">
                          <h5 className="font-bold text-gray-900 mb-1">{title}</h5>
                          {description && <p className="text-sm text-gray-700">{description}</p>}
                        </div>
                      </div>
                    </div>
                  );
                }

                // Bullet points (*, -, •)
                if (trimmed.match(/^\s*[\*\-•]\s+/)) {
                  const match = trimmed.match(/^\s*[\*\-•]\s+\*\*(.+?)\*\*:?\s*(.*)/) || trimmed.match(/^\s*[\*\-•]\s+(.+)/);
                  const label = match[1]?.replace(':', '').trim() || '';
                  const text = match[2]?.trim() || match[0]?.replace(/^\s*[\*\-•]\s+/, '').trim();
                  
                  return (
                    <div key={idx} className="flex items-start gap-3 ml-12 py-1">
                      <CheckCircle className="w-4 h-4 text-blue-600 flex-shrink-0 mt-1" />
                      <p className="text-sm text-gray-700 flex-1">
                        {label && <span className="font-semibold">{label}: </span>}
                        {text}
                      </p>
                    </div>
                  );
                }

                // Regular paragraph
                return (
                  <p key={idx} className="text-gray-700 leading-relaxed ml-4">
                    {trimmed.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').split(/<strong>|<\/strong>/).map((part, i) => 
                      i % 2 === 0 ? part : <strong key={i} className="font-semibold">{part}</strong>
                    )}
                  </p>
                );
              })}
            </div>

            {/* Quick Summary Badge */}
            <div className="mt-8 flex items-center justify-center">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-full shadow-lg">
                <Zap className="w-4 h-4" />
                <span className="text-sm font-medium">AI-Powered Analysis Complete</span>
              </div>
            </div>
          </div>
        )}
        </>
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

      {/* Disclaimer */}
      <div className="text-center text-xs text-gray-400 mt-8">
        <p>Disclaimer: AI analysis is for informational purposes only and not financial advice. Consult a professional financial advisor before making investment decisions.</p>
      </div>
      </>
      )}
    </div>
  );
}
