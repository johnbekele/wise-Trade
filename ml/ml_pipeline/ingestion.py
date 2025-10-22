from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from sre_constants import IN
from typing import Optional


import pandas as pd
import requests
import ssl
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for development (not recommended for production)
urllib3.disable_warnings(InsecureRequestWarning)


import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from app.core.config import settings

@dataclass
class IngestionConfig:
    symbol: str
    start_date: Optional[str] = None  # YYYY-MM-DD
    end_date: Optional[str] = None    # YYYY-MM-DD
    raw_dir: Path = Path("ml/data/raw")


def fetch_news(config: IngestionConfig) -> Path:
    payload={
  "action": "getArticles",
  "keyword": "Tesla Inc",
  "sourceLocationUri": [
    "http://en.wikipedia.org/wiki/United_States",
    "http://en.wikipedia.org/wiki/Canada",
    "http://en.wikipedia.org/wiki/United_Kingdom"
  ],
  "ignoreSourceGroupUri": "paywall/paywalled_sources",
  "articlesPage": 1,
  "articlesCount": 100,
  "articlesSortBy": "date",
  "articlesSortByAsc": False,
  "dataType": [
    "news",
    "pr"
  ],
  "forceMaxDataTimeWindow": 31,
  "resultType": "articles",
  "apiKey": settings.NEWS_API_KEY
}
    try:
        # Use verify=False to bypass SSL certificate verification for development
        # In production, you should properly configure SSL certificates
        response = requests.get(f"{settings.NEWS_API_URL}/article/getArticles", 
                              json=payload, 
                              verify=False,
                              timeout=30)
        response.raise_for_status()
        data = response.json()
        # Initialize the data structure with empty lists
        ready_data = {
            "title": [],
            "content": [],
            "publishedAt": []
        }
        
        articles = data.get('articles', {}).get('results', [])
        print(f"Successfully fetched {len(articles)} articles")
        
        # Process each article
        for article in articles:
            # Extract article data with fallbacks for missing fields
            title = article.get('title', 'No Title')
            content = article.get('body', article.get('content', 'No Content'))
            published_at = article.get('date', article.get('publishedAt', 'No Date'))
            
            ready_data["title"].append(title)
            ready_data["content"].append(content)
            ready_data["publishedAt"].append(published_at)
        
        # Create DataFrame and display results
        clean_data = pd.DataFrame(ready_data)
        print(f"\nDataFrame shape: {clean_data.shape}")
        print("\nFirst 5 articles:")
        print(clean_data)
        
        # Save data to CSV file
        output_file = config.raw_dir / f"news_data_{config.symbol}_{config.start_date}_{config.end_date}.csv"
        config.raw_dir.mkdir(parents=True, exist_ok=True)
        clean_data.to_csv(output_file, index=False)
        print(f"\nData saved to: {output_file}")
        
        return clean_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None

    


ingested_data=IngestionConfig(symbol="AAPL", start_date="2024-01-01", end_date="2024-12-31")
fetch_news(ingested_data)

