from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Optional, Any
from app.services.yahoo_finance_service import YahooFinanceService
from app.core.api_key_auth import authenticate_user_or_api_key

router = APIRouter()

# Lazy initialization to ensure settings are loaded
def get_stock_service():
    return YahooFinanceService()

@router.get("/quote/{symbol}")
async def get_quote(symbol: str, auth: Dict[str, Any] = Depends(authenticate_user_or_api_key)):
    """Get real-time quote for a stock symbol."""
    stock_service = get_stock_service()
    data = stock_service.get_quote(symbol.upper())
    
    # Service now returns mock data instead of errors when rate limited
    # Transform Yahoo Finance data to consistent format
    return {
        "symbol": symbol.upper(),
        "data": {
            "Global Quote": {
                "01. symbol": symbol.upper(),
                "02. open": str(data.get("regularMarketOpen", 0)),
                "03. high": str(data.get("regularMarketDayHigh", 0)),
                "04. low": str(data.get("regularMarketDayLow", 0)),
                "05. price": str(data.get("regularMarketPrice", 0)),
                "06. volume": str(data.get("regularMarketVolume", 0)),
                "07. latest trading day": "",
                "08. previous close": str(data.get("regularMarketPreviousClose", 0)),
                "09. change": str(data.get("regularMarketChange", 0)),
                "10. change percent": f"{data.get('regularMarketChangePercent', 0):.2f}%"
            }
        }
    }


@router.get("/candles/{symbol}")
async def get_candles(
    symbol: str,
    resolution: str = Query("1d", description="Candle resolution: 1m, 5m, 15m, 30m, 1h, 1d"),
    days: int = Query(30, description="Number of days to look back"),
    auth: Dict[str, Any] = Depends(authenticate_user_or_api_key)
):
    """Get candlestick data for charts."""
    # Yahoo Finance RapidAPI doesn't have a chart endpoint
    # Return empty data for now - quotes work, but historical data isn't available in this API
    return {
        "symbol": symbol.upper(),
        "data": {
            f"Time Series ({resolution})": {}
        }
    }


@router.get("/profile/{symbol}")
async def get_profile(symbol: str, auth: Dict[str, Any] = Depends(authenticate_user_or_api_key)):
    """Get company profile and information."""
    stock_service = get_stock_service()
    # Yahoo Finance RapidAPI doesn't have a separate profile endpoint
    # Get basic info from quote instead
    quote_data = stock_service.get_quote(symbol.upper())
    
    if "error" in quote_data:
        # Return minimal profile data
        return {
            "symbol": symbol.upper(),
            "data": {
                "Symbol": symbol.upper(),
                "Name": symbol.upper(),
                "Description": f"{symbol.upper()} stock information",
                "Country": "US",
                "Sector": "N/A",
                "Industry": "N/A",
                "MarketCapitalization": "0",
                "PERatio": "N/A",
                "52WeekHigh": "N/A",
                "52WeekLow": "N/A",
                "Exchange": "NASDAQ",
                "Currency": "USD",
                "Logo": ""
            }
        }
    
    # Use data from quote
    return {
        "symbol": symbol.upper(),
        "data": {
            "Symbol": symbol.upper(),
            "Name": quote_data.get("longName", quote_data.get("shortName", symbol.upper())),
            "Description": f"{quote_data.get('longName', symbol.upper())} - {quote_data.get('fullExchangeName', 'Stock Exchange')}",
            "Country": "US",
            "Sector": "N/A",
            "Industry": "N/A",
            "MarketCapitalization": "0",
            "PERatio": "N/A",
            "52WeekHigh": "N/A",
            "52WeekLow": "N/A",
            "Exchange": quote_data.get("fullExchangeName", "NASDAQ"),
            "Currency": "USD",
            "Logo": ""
        }
    }


@router.get("/search")
async def search_stocks(keywords: str = Query(..., min_length=1), auth: Dict[str, Any] = Depends(authenticate_user_or_api_key)):
    """Search for stocks by symbol or company name."""
    stock_service = get_stock_service()
    data = stock_service.search_symbol(keywords)
    
    if "error" in data:
        raise HTTPException(status_code=500, detail=f"Error searching stocks: {data['error']}")
    
    # Transform results
    results = []
    quotes = data.get("quotes", [])
    
    for item in quotes[:10]:
        results.append({
            "symbol": item.get("symbol", ""),
            "name": item.get("longname", item.get("shortname", "")),
            "type": item.get("quoteType", ""),
            "region": item.get("exchDisp", "")
        })
    
    return {"results": results}


@router.get("/market-movers")
async def get_market_movers(auth: Dict[str, Any] = Depends(authenticate_user_or_api_key)):
    """Get top gainers, losers, and most active stocks."""
    stock_service = get_stock_service()
    data = stock_service.get_market_movers()
    
    if "error" in data:
        raise HTTPException(status_code=500, detail=f"Error fetching market movers: {data['error']}")
    
    # Transform to expected format
    def format_stock(stock):
        return {
            "ticker": stock.get("symbol", ""),
            "price": f"{stock.get('regularMarketPrice', 0):.2f}",
            "change_amount": f"{stock.get('regularMarketChange', 0):.2f}",
            "change_percentage": f"{stock.get('regularMarketChangePercent', 0):.2f}%",
            "volume": str(stock.get("regularMarketVolume", 0))
        }
    
    return {
        "top_gainers": [format_stock(s) for s in data.get("gainers", [])],
        "top_losers": [format_stock(s) for s in data.get("losers", [])],
        "most_actively_traded": [format_stock(s) for s in data.get("most_active", [])]
    }
