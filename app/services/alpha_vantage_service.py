import requests
import urllib3
from typing import Dict, Optional, List
from app.core.config import settings

# Disable SSL warnings for development environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AlphaVantageService:
    """Service to fetch stock market data from Alpha Vantage API"""
    
    def __init__(self):
        self.api_key = settings.ALPHA_VANTAGE_API_KEY
        self.base_url = settings.ALPHA_VANTAGE_API_URL or "https://www.alphavantage.co/query"
        self.verify_ssl = True
    
    def _make_request(self, params: Dict) -> Dict:
        """
        Make a request to Alpha Vantage API
        
        Args:
            params: Query parameters for the API request
        
        Returns:
            Dictionary containing API response
        """
        params["apikey"] = self.api_key
        
        try:
            # Try with SSL verification first
            try:
                response = requests.get(self.base_url, params=params, timeout=10, verify=self.verify_ssl)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.SSLError:
                # If SSL verification fails, retry without verification
                self.verify_ssl = False
                response = requests.get(self.base_url, params=params, timeout=10, verify=False)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "data": None}
    
    def get_global_quote(self, symbol: str) -> Dict:
        """
        Get latest real-time quote (price, change %, volume)
        
        Args:
            symbol: Stock ticker symbol (e.g., "AAPL", "TSLA")
        
        Returns:
            Dictionary containing current stock quote
        """
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol.upper()
        }
        return self._make_request(params)
    
    def get_intraday_data(self, symbol: str, interval: str = "5min", outputsize: str = "compact") -> Dict:
        """
        Get intraday time series data (1min, 5min, 15min, 30min, 60min)
        
        Args:
            symbol: Stock ticker symbol
            interval: Time interval between data points (1min, 5min, 15min, 30min, 60min)
            outputsize: "compact" (100 data points) or "full" (full-length intraday data)
        
        Returns:
            Dictionary containing intraday time series data
        """
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol.upper(),
            "interval": interval,
            "outputsize": outputsize
        }
        return self._make_request(params)
    
    def get_daily_data(self, symbol: str, outputsize: str = "compact") -> Dict:
        """
        Get daily time series data with adjusted close prices
        
        Args:
            symbol: Stock ticker symbol
            outputsize: "compact" (100 days) or "full" (20+ years)
        
        Returns:
            Dictionary containing daily time series data
        """
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol.upper(),
            "outputsize": outputsize
        }
        return self._make_request(params)
    
    def get_weekly_data(self, symbol: str) -> Dict:
        """
        Get weekly time series data with adjusted close prices
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary containing weekly time series data
        """
        params = {
            "function": "TIME_SERIES_WEEKLY_ADJUSTED",
            "symbol": symbol.upper()
        }
        return self._make_request(params)
    
    def search_symbol(self, keywords: str) -> Dict:
        """
        Search for stock symbols based on keywords
        
        Args:
            keywords: Search keywords (company name or ticker)
        
        Returns:
            Dictionary containing search results with matching symbols
        """
        params = {
            "function": "SYMBOL_SEARCH",
            "keywords": keywords
        }
        return self._make_request(params)
    
    def get_company_overview(self, symbol: str) -> Dict:
        """
        Get company fundamental data and financial ratios
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary containing company overview data
        """
        params = {
            "function": "OVERVIEW",
            "symbol": symbol.upper()
        }
        return self._make_request(params)
    
    def get_top_gainers_losers(self) -> Dict:
        """
        Get top gainers, losers, and most actively traded tickers
        
        Returns:
            Dictionary containing market movers data
        """
        params = {
            "function": "TOP_GAINERS_LOSERS"
        }
        return self._make_request(params)
    
    def get_multiple_quotes(self, symbols: List[str]) -> List[Dict]:
        """
        Get quotes for multiple symbols
        
        Args:
            symbols: List of stock ticker symbols
        
        Returns:
            List of dictionaries containing quote data for each symbol
        """
        results = []
        for symbol in symbols:
            quote = self.get_global_quote(symbol)
            results.append({
                "symbol": symbol,
                "data": quote
            })
        return results
    
    def get_market_status(self) -> Dict:
        """
        Get current market status (open/closed)
        
        Returns:
            Dictionary containing market status information
        """
        params = {
            "function": "MARKET_STATUS"
        }
        return self._make_request(params)

