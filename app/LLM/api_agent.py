from langchain_core.tools import tool
from typing import Optional
import json

from app.core.genAI import GenAI
from app.services.news_service import NewsService
from app.core.config import settings


# Initialize services
news_service = NewsService()
genai_instance = GenAI()


@tool
def fetch_top_financial_headlines(category: Optional[str] = None, page_size: int = 20) -> str:
    """
    Fetch top financial/business headlines that could affect the stock market.
    
    Args:
        category: Category of news (business, technology, general). Defaults to business.
        page_size: Number of articles to fetch (max 100). Defaults to 20.
    
    Returns:
        JSON string containing top financial headlines with titles, descriptions, sources, and publication dates.
    """
    if not category:
        category = "business"
    
    result = news_service.fetch_top_headlines(
        category=category,
        country="us",
        page_size=page_size
    )
    
    if "error" in result:
        return json.dumps({"error": result["error"]})
    
    articles = result.get("articles", [])
    key_info = news_service.extract_key_info(articles)
    
    return json.dumps({
        "status": "success",
        "total_results": result.get("totalResults", 0),
        "articles": key_info
    }, indent=2)


@tool
def search_financial_news(query: str, page_size: int = 20) -> str:
    """
    Search for financial news articles based on keywords or topics.
    Use this to find news about specific companies, sectors, or market events.
    
    Args:
        query: Search keywords (e.g., "Apple earnings", "Federal Reserve", "tech stocks")
        page_size: Number of articles to fetch (max 100). Defaults to 20.
    
    Returns:
        JSON string containing relevant financial news articles with titles, descriptions, sources, and publication dates.
    """
    result = news_service.fetch_financial_news(query=query, page_size=page_size)
    
    if "error" in result:
        return json.dumps({"error": result["error"]})
    
    articles = result.get("articles", [])
    key_info = news_service.extract_key_info(articles)
    
    return json.dumps({
        "status": "success",
        "total_results": result.get("totalResults", 0),
        "query": query,
        "articles": key_info
    }, indent=2)


@tool
def fetch_stock_news(symbol: str, page_size: int = 20) -> str:
    """
    Fetch news articles specific to a stock ticker symbol.
    Use this to get the latest news about a particular company that could affect its stock price.
    
    Args:
        symbol: Stock ticker symbol (e.g., "AAPL", "TSLA", "MSFT")
        page_size: Number of articles to fetch (max 100). Defaults to 20.
    
    Returns:
        JSON string containing stock-specific news articles with titles, descriptions, sources, and publication dates.
    """
    result = news_service.fetch_stock_specific_news(symbol=symbol.upper(), page_size=page_size)
    
    if "error" in result:
        return json.dumps({"error": result["error"]})
    
    articles = result.get("articles", [])
    key_info = news_service.extract_key_info(articles)
    
    return json.dumps({
        "status": "success",
        "symbol": symbol.upper(),
        "total_results": result.get("totalResults", 0),
        "articles": key_info
    }, indent=2)


class APIAgent:
    """Agent that analyzes financial news and identifies information affecting stock markets"""
    
    def __init__(self):
        self.genai_instance = GenAI()
        self.news_service = NewsService()
        
        # Define tools (kept for reference, but not used with LangChain agent anymore)
        self.tools = [
            fetch_top_financial_headlines,
            search_financial_news,
            fetch_stock_news,
        ]
    
    def analyze_market_news(self, query: str) -> str:
        """
        Analyze financial news and identify information affecting stock markets
        
        Args:
            query: User query about what news to analyze (e.g., "Find news about tech stocks", 
                   "What's affecting Apple stock?", "Latest market-moving news")
        
        Returns:
            Analysis of news and its potential market impact
        """
        # Fetch news based on query
        news_result = self.news_service.fetch_financial_news(query=query, page_size=20)
        articles = news_result.get("articles", [])
        
        if not articles:
            return "No news articles found for the given query."
        
        # Prepare news summary
        news_summary = "\n\n".join([
            f"Title: {art.get('title', 'N/A')}\n"
            f"Description: {art.get('description', 'N/A')}\n"
            f"Source: {art.get('source', {}).get('name', 'N/A')}\n"
            f"Published: {art.get('publishedAt', 'N/A')}"
            for art in articles[:10]
        ])
        
        # Use LLM to analyze
        prompt = f"""Analyze the following financial news and identify information that could significantly affect stock markets.

User Query: {query}

News Articles:
{news_summary}

Please provide:
1. Most impactful news items and why they matter
2. Which companies or sectors are affected
3. Potential market impact (high/medium/low) and direction (positive/negative)
4. Actionable insights for traders"""
        
        # Use Google AI SDK directly
        try:
            return self.genai_instance.generate_content_direct(prompt, temperature=0.7)
        except Exception as e:
            return f"Error during LLM analysis: {str(e)[:200]}"
    
    def find_market_impact_news(self, limit: int = 10) -> str:
        """
        Find the most impactful financial news that could affect stock markets
        
        Args:
            limit: Maximum number of news items to analyze
        
        Returns:
            Analysis of top market-impacting news
        """
        # Fetch top financial headlines directly instead of searching with a query
        news_result = self.news_service.fetch_top_headlines(
            category="business",
            country="us",
            page_size=limit * 2  # Get more articles to analyze and filter
        )
        
        articles = news_result.get("articles", [])
        
        if not articles:
            # Try fetching general business news without category filter
            news_result = self.news_service.fetch_top_headlines(
                country="us",
                page_size=limit * 2
            )
            articles = news_result.get("articles", [])
        
        if not articles:
            return "No news articles found. Please check your News API connection and API key."
        
        # Prepare news summary
        news_summary = "\n\n".join([
            f"Title: {art.get('title', 'N/A')}\n"
            f"Description: {art.get('description', 'N/A')}\n"
            f"Source: {art.get('source', {}).get('name', 'N/A')}\n"
            f"Published: {art.get('publishedAt', 'N/A')}"
            for art in articles[:limit * 2]
        ])
        
        # Use LLM to analyze and identify most impactful news
        # Use Google AI SDK directly to avoid max_retries compatibility issues with LangChain
        prompt = f"""Analyze the following financial news articles and identify the top {limit} most impactful items that could significantly affect stock markets.

Focus on:
- Breaking news and major announcements
- Earnings reports and financial results
- Economic indicators and policy changes
- Company-specific news (mergers, product launches, regulatory changes)
- Sector-wide trends

News Articles:
{news_summary}

Please provide:
1. Top {limit} most impactful news items ranked by potential market impact
2. For each item: explain why it matters and potential market impact (high/medium/low)
3. Which companies or sectors are most affected
4. Potential price impact direction (positive/negative/neutral)
5. Actionable insights for traders

Format your response clearly with numbered items."""
        
        # Use Google AI SDK directly
        try:
            return self.genai_instance.generate_content_direct(prompt, temperature=0.7)
        except Exception as e:
            return f"Error during LLM analysis: {str(e)[:200]}"


# Create a global agent instance
agent = APIAgent()
