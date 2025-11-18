from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from app.services.alpha_vantage_service import AlphaVantageService

router = APIRouter()
stock_service = AlphaVantageService()


class StockQuoteResponse(BaseModel):
    symbol: str
    data: dict


class SymbolSearchRequest(BaseModel):
    keywords: str


@router.get("/quote/{symbol}")
async def get_stock_quote(symbol: str):
    """Get real-time quote for a stock symbol"""
    try:
        data = stock_service.get_global_quote(symbol)
        if "error" in data or "Error Message" in data:
            raise HTTPException(status_code=404, detail=f"Symbol not found or API error: {data.get('error', data.get('Error Message'))}")
        return {"symbol": symbol.upper(), "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quote: {str(e)}")


@router.get("/intraday/{symbol}")
async def get_intraday_data(
    symbol: str,
    interval: str = Query("5min", regex="^(1min|5min|15min|30min|60min)$"),
    outputsize: str = Query("compact", regex="^(compact|full)$")
):
    """Get intraday time series data for a stock"""
    try:
        data = stock_service.get_intraday_data(symbol, interval, outputsize)
        if "error" in data or "Error Message" in data:
            raise HTTPException(status_code=404, detail=f"Error fetching intraday data: {data.get('error', data.get('Error Message'))}")
        return {"symbol": symbol.upper(), "interval": interval, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching intraday data: {str(e)}")


@router.get("/daily/{symbol}")
async def get_daily_data(
    symbol: str,
    outputsize: str = Query("compact", regex="^(compact|full)$")
):
    """Get daily time series data for a stock"""
    try:
        data = stock_service.get_daily_data(symbol, outputsize)
        if "error" in data or "Error Message" in data:
            raise HTTPException(status_code=404, detail=f"Error fetching daily data: {data.get('error', data.get('Error Message'))}")
        return {"symbol": symbol.upper(), "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching daily data: {str(e)}")


@router.get("/weekly/{symbol}")
async def get_weekly_data(symbol: str):
    """Get weekly time series data for a stock"""
    try:
        data = stock_service.get_weekly_data(symbol)
        if "error" in data or "Error Message" in data:
            raise HTTPException(status_code=404, detail=f"Error fetching weekly data: {data.get('error', data.get('Error Message'))}")
        return {"symbol": symbol.upper(), "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weekly data: {str(e)}")


@router.get("/search")
async def search_symbol(keywords: str = Query(..., min_length=1)):
    """Search for stock symbols by keywords"""
    try:
        data = stock_service.search_symbol(keywords)
        if "error" in data or "Error Message" in data:
            raise HTTPException(status_code=404, detail=f"Error searching symbols: {data.get('error', data.get('Error Message'))}")
        return {"keywords": keywords, "results": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching symbols: {str(e)}")


@router.get("/overview/{symbol}")
async def get_company_overview(symbol: str):
    """Get company fundamental data and overview"""
    try:
        data = stock_service.get_company_overview(symbol)
        if "error" in data or "Error Message" in data:
            raise HTTPException(status_code=404, detail=f"Error fetching overview: {data.get('error', data.get('Error Message'))}")
        return {"symbol": symbol.upper(), "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company overview: {str(e)}")


@router.get("/market-movers")
async def get_market_movers():
    """Get top gainers, losers, and most actively traded stocks"""
    try:
        data = stock_service.get_top_gainers_losers()
        if "error" in data or "Error Message" in data:
            raise HTTPException(status_code=404, detail=f"Error fetching market movers: {data.get('error', data.get('Error Message'))}")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market movers: {str(e)}")


@router.get("/market-status")
async def get_market_status():
    """Get current market status"""
    try:
        data = stock_service.get_market_status()
        if "error" in data or "Error Message" in data:
            raise HTTPException(status_code=404, detail=f"Error fetching market status: {data.get('error', data.get('Error Message'))}")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market status: {str(e)}")


@router.post("/quotes/batch")
async def get_multiple_quotes(symbols: List[str]):
    """Get quotes for multiple symbols"""
    try:
        if len(symbols) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 symbols allowed per request")
        data = stock_service.get_multiple_quotes(symbols)
        return {"symbols": symbols, "quotes": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quotes: {str(e)}")

