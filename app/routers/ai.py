from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.LLM.api_agent import agent

router = APIRouter()


class NewsAnalysisRequest(BaseModel):
    query: str
    limit: Optional[int] = 10


class NewsAnalysisResponse(BaseModel):
    analysis: str
    query: str


# Path parameter route must come BEFORE query parameter route
@router.get("/analyze-news/{query}", response_model=NewsAnalysisResponse)
async def analyze_news_path(query: str):
    """Analyze financial news for market impact (GET with path parameter)
    
    Usage: GET /api/ai/analyze-news/tesla
    """
    try:
        analysis = agent.analyze_market_news(query)
        return NewsAnalysisResponse(analysis=analysis, query=query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing news: {str(e)}")


@router.get("/analyze-news", response_model=NewsAnalysisResponse)
async def analyze_news_get(query: str):
    """Analyze financial news for market impact (GET with query parameter)
    
    Usage: GET /api/ai/analyze-news?query=tesla
    """
    try:
        analysis = agent.analyze_market_news(query)
        return NewsAnalysisResponse(analysis=analysis, query=query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing news: {str(e)}")


@router.post("/analyze-news", response_model=NewsAnalysisResponse)
async def analyze_news_post(request: NewsAnalysisRequest):
    """Analyze financial news for market impact (POST with JSON body)"""
    try:
        analysis = agent.analyze_market_news(request.query)
        return NewsAnalysisResponse(analysis=analysis, query=request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing news: {str(e)}")


@router.get("/market-impact", response_model=NewsAnalysisResponse)
async def get_market_impact_news(limit: int = 10):
    """Get the most impactful financial news affecting stock markets"""
    try:
        analysis = agent.find_market_impact_news(limit=limit)
        return NewsAnalysisResponse(
            analysis=analysis,
            query=f"Top {limit} market-impacting news"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market impact news: {str(e)}")
