import requests
import urllib3
from typing import List, Dict, Optional
from app.core.config import settings

# Disable SSL warnings for development environments (WSL/common SSL cert issues)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NewsService:
    """Service to fetch news from News API"""
    
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.base_url = settings.NEWS_API_URL or "https://newsapi.org/v2"
        # Try to verify SSL, but fallback to False if certificates are missing (WSL issue)
        self.verify_ssl = True
    
    def fetch_top_headlines(self, 
                           category: Optional[str] = None,
                           country: str = "us",
                           query: Optional[str] = None,
                           page_size: int = 20) -> Dict:
        """
        Fetch top headlines from News API
        
        Args:
            category: Category of news (business, technology, general, etc.)
            country: Country code (default: us)
            query: Search query/keywords
            page_size: Number of articles to fetch (max 100)
        
        Returns:
            Dictionary containing articles and metadata
        """
        url = f"{self.base_url}/top-headlines"
        params = {
            "apiKey": self.api_key,
            "pageSize": min(page_size, 100),
        }
        
        if category:
            params["category"] = category
        if country:
            params["country"] = country
        if query:
            params["q"] = query
        
        try:
            # Try with SSL verification first
            try:
                response = requests.get(url, params=params, timeout=10, verify=self.verify_ssl)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.SSLError:
                # If SSL verification fails, retry without verification (WSL/common issue)
                self.verify_ssl = False
                response = requests.get(url, params=params, timeout=10, verify=False)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "articles": []}
    
    def fetch_everything(self,
                        query: str,
                        sort_by: str = "publishedAt",
                        language: str = "en",
                        page_size: int = 20,
                        from_date: Optional[str] = None,
                        to_date: Optional[str] = None) -> Dict:
        """
        Fetch all articles matching a query
        
        Args:
            query: Search query/keywords
            sort_by: Sort order (relevancy, popularity, publishedAt)
            language: Language code (default: en)
            page_size: Number of articles to fetch (max 100)
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
        
        Returns:
            Dictionary containing articles and metadata
        """
        url = f"{self.base_url}/everything"
        params = {
            "apiKey": self.api_key,
            "q": query,
            "sortBy": sort_by,
            "language": language,
            "pageSize": min(page_size, 100),
        }
        
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        
        try:
            # Try with SSL verification first
            try:
                response = requests.get(url, params=params, timeout=10, verify=self.verify_ssl)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.SSLError:
                # If SSL verification fails, retry without verification (WSL/common issue)
                self.verify_ssl = False
                response = requests.get(url, params=params, timeout=10, verify=False)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "articles": []}
    
    def fetch_financial_news(self, query: Optional[str] = None, page_size: int = 20) -> Dict:
        """
        Fetch financial/business news
        
        Args:
            query: Optional search query
            page_size: Number of articles to fetch
        
        Returns:
            Dictionary containing financial news articles
        """
        if query:
            return self.fetch_everything(
                query=f"{query} finance OR stock OR market OR trading",
                sort_by="publishedAt",
                page_size=page_size
            )
        else:
            return self.fetch_top_headlines(
                category="business",
                page_size=page_size
            )
    
    def fetch_stock_specific_news(self, symbol: str, page_size: int = 20) -> Dict:
        """
        Fetch news specific to a stock symbol
        
        Args:
            symbol: Stock ticker symbol (e.g., AAPL, TSLA)
            page_size: Number of articles to fetch
        
        Returns:
            Dictionary containing stock-specific news articles
        """
        return self.fetch_everything(
            query=f"{symbol} stock OR company OR earnings",
            sort_by="publishedAt",
            page_size=page_size
        )
    
    def extract_key_info(self, articles: List[Dict]) -> List[Dict]:
        """
        Extract key information from articles
        
        Args:
            articles: List of article dictionaries
        
        Returns:
            List of dictionaries with extracted key information
        """
        key_info = []
        for article in articles:
            key_info.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "source": article.get("source", {}).get("name", ""),
                "publishedAt": article.get("publishedAt", ""),
                "url": article.get("url", ""),
            })
        return key_info

