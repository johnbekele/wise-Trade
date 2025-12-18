from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
from app.LLM.api_agent import agent
from app.core.api_key_auth import check_ai_access_with_api_key

router = APIRouter()
bearer_scheme = HTTPBearer(auto_error=False)


class NewsAnalysisRequest(BaseModel):
    query: str
    limit: Optional[int] = 10


class NewsAnalysisResponse(BaseModel):
    analysis: str
    query: str


@router.get("/analyze-news/{query}", response_model=NewsAnalysisResponse)
async def analyze_news_path(query: str, auth: Dict[str, Any] = Depends(check_ai_access_with_api_key)):
    # Analyze news with path parameter
    try:
        loop = asyncio.get_event_loop()
        analysis = await loop.run_in_executor(None, agent.analyze_market_news, query)
        return NewsAnalysisResponse(analysis=analysis, query=query)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing news: {str(e)}")


@router.get("/analyze-news", response_model=NewsAnalysisResponse)
async def analyze_news_get(query: str, auth: Dict[str, Any] = Depends(check_ai_access_with_api_key)):
    # Analyze news with query parameter
    try:
        loop = asyncio.get_event_loop()
        analysis = await loop.run_in_executor(None, agent.analyze_market_news, query)
        return NewsAnalysisResponse(analysis=analysis, query=query)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing news: {str(e)}")


@router.post("/analyze-news", response_model=NewsAnalysisResponse)
async def analyze_news_post(request: NewsAnalysisRequest, auth: Dict[str, Any] = Depends(check_ai_access_with_api_key)):
    # Analyze news with JSON body
    try:
        loop = asyncio.get_event_loop()
        analysis = await loop.run_in_executor(None, agent.analyze_market_news, request.query)
        return NewsAnalysisResponse(analysis=analysis, query=request.query)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing news: {str(e)}")


@router.get("/market-impact")
async def get_market_impact_news(limit: int = 10, auth: Dict[str, Any] = Depends(check_ai_access_with_api_key)):
    # Get market impact news
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, agent.find_market_impact_news, limit)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market impact news: {str(e)}")
