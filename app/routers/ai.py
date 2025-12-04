from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import asyncio
from app.LLM.api_agent import agent
from app.core.security import security_manager
from app.repositories.users_repository import UsersRepository

router = APIRouter()
bearer_scheme = HTTPBearer(auto_error=False)


def get_users_repository() -> UsersRepository:
    return UsersRepository()


async def check_ai_access(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    users_repo: UsersRepository = Depends(get_users_repository)
):
    # Check if user has AI access
    if not credentials:
        return None
    
    token = credentials.credentials
    result = security_manager.decode_token(token)
    
    if not result.get("success"):
        return None
    
    payload = result.get("payload", {})
    user_id = payload.get("sub")
    
    if not user_id:
        return None
    
    user = await users_repo.find_by_id(user_id)
    if not user:
        return None
    
    if getattr(user, 'ai_access_blocked', False):
        raise HTTPException(status_code=403, detail="Your AI access has been blocked. Please contact an administrator.")
    
    return user


class NewsAnalysisRequest(BaseModel):
    query: str
    limit: Optional[int] = 10


class NewsAnalysisResponse(BaseModel):
    analysis: str
    query: str


@router.get("/analyze-news/{query}", response_model=NewsAnalysisResponse)
async def analyze_news_path(query: str, user=Depends(check_ai_access)):
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
async def analyze_news_get(query: str, user=Depends(check_ai_access)):
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
async def analyze_news_post(request: NewsAnalysisRequest, user=Depends(check_ai_access)):
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
async def get_market_impact_news(limit: int = 10, user=Depends(check_ai_access)):
    # Get market impact news
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, agent.find_market_impact_news, limit)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market impact news: {str(e)}")
