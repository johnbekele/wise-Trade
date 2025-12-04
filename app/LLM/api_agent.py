"""
API Agent using Claude AI with Code Agent SDK
Agent-based implementation for autonomous news fetching and analysis
"""
from typing import Optional, Dict, Any, List
import json
from functools import lru_cache
from datetime import datetime, timedelta

from app.core.claudeAI import ClaudeAI
from app.services.news_service import NewsService
from app.core.config import settings


# Initialize services
news_service = NewsService()
claude_ai = ClaudeAI()

# Simple in-memory cache with TTL
_cache = {}
_cache_ttl = {}


def get_claude_tools() -> List[Dict[str, Any]]:
    """
    Define Claude tools (skills) for API fetching and analysis
    
    Returns:
        List of tool definitions for Claude to use
    """
    return [
        {
            "name": "fetch_top_financial_headlines",
            "description": "Fetch top financial/business headlines that could affect the stock market. Use this to get the latest market-moving news.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category of news (business, technology, general). Defaults to business.",
                        "enum": ["business", "technology", "general"]
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of articles to fetch (max 100). Defaults to 20.",
                        "minimum": 1,
                        "maximum": 100
                    }
                }
            }
        },
        {
            "name": "search_financial_news",
            "description": "Search for financial news articles based on keywords or topics. Use this to find news about specific companies, sectors, or market events.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keywords (e.g., 'Apple earnings', 'Federal Reserve', 'tech stocks')"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of articles to fetch (max 100). Defaults to 20.",
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "fetch_stock_news",
            "description": "Fetch news articles specific to a stock ticker symbol. Use this to get the latest news about a particular company that could affect its stock price.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'MSFT')"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of articles to fetch (max 100). Defaults to 20.",
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["symbol"]
            }
        }
    ]


def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> str:
    """
    Execute a tool/skill and return the result
    
    Args:
        tool_name: Name of the tool to execute
        tool_input: Input parameters for the tool
    
    Returns:
        JSON string with tool execution results
    """
    try:
        if tool_name == "fetch_top_financial_headlines":
            category = tool_input.get("category", "business")
            page_size = tool_input.get("page_size", 20)
            
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
        
        elif tool_name == "search_financial_news":
            query = tool_input.get("query", "")
            page_size = tool_input.get("page_size", 20)
            
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
        
        elif tool_name == "fetch_stock_news":
            symbol = tool_input.get("symbol", "").upper()
            page_size = tool_input.get("page_size", 20)
            
            result = news_service.fetch_stock_specific_news(symbol=symbol, page_size=page_size)
            
            if "error" in result:
                return json.dumps({"error": result["error"]})
            
            articles = result.get("articles", [])
            key_info = news_service.extract_key_info(articles)
            
            return json.dumps({
                "status": "success",
                "symbol": symbol,
                "total_results": result.get("totalResults", 0),
                "articles": key_info
            }, indent=2)
        
        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})
    
    except Exception as e:
        return json.dumps({"error": f"Tool execution failed: {str(e)}"})


class APIAgent:
    """Agent that autonomously analyzes financial news using Claude AI with Code Agent SDK"""
    
    def __init__(self):
        self.claude_ai = ClaudeAI()
        self.news_service = NewsService()
        self.tools = get_claude_tools()
    
    def analyze_market_news(self, query: str) -> str:
        """
        Analyze financial news using agent-based approach (optimized for speed)
        Agent autonomously decides which tools to use and when
        
        Args:
            query: User query about what news to analyze (e.g., "Find news about tech stocks", 
                   "What's affecting Apple stock?", "Latest market-moving news")
        
        Returns:
            Analysis of news and its potential market impact in formatted markdown-style text
        """
        # Check cache first (5 minute TTL)
        cache_key = f"analyze_{query.lower().strip()}"
        if cache_key in _cache:
            if datetime.now() < _cache_ttl.get(cache_key, datetime.now()):
                return _cache[cache_key]
        
        system_prompt = """You are an expert financial analyst AI agent. Your role is to:
1. Use available tools to fetch relevant financial news based on user queries
2. Analyze the fetched news to identify market-moving events
3. Provide comprehensive insights in a structured format

IMPORTANT: Format your response using markdown-style structure that the frontend can parse:
- Use section headers: "### 1. Most Impactful News Items" or "1. Most Impactful News Items"
- Use numbered items with bold titles: "1. **News Title**" followed by description
- Use bullet points for details: "* Why it matters: ..." or "- Impact: ..."
- Use clear paragraphs for explanations

Structure your response with these sections:
1. Most Impactful News Items and Why They Matter
2. Which Companies or Sectors Are Affected
3. Potential Market Impact (high/medium/low) and Direction (positive/negative)
4. Actionable Insights for Traders

IMPORTANT: Be concise and efficient. Use tools only when necessary. Complete your analysis quickly."""
        
        try:
            # Optimized: Reduce iterations and tokens for faster response
            response = self.claude_ai.run_agent(
                user_message=query,
                tools=self.tools,
                tool_executor=execute_tool,
                system=system_prompt,
                max_iterations=5,  # Reduced from 10 to 5 for speed
                temperature=0.7,
                max_tokens=2048  # Reduced from 4096 for faster generation
            )
            
            # Ensure response is properly formatted
            if not response or len(response.strip()) == 0:
                return "No analysis could be generated. Please try a different query."
            
            # Cache the response
            _cache[cache_key] = response
            _cache_ttl[cache_key] = datetime.now() + timedelta(minutes=5)
            
            return response
        
        except Exception as e:
            return f"Error during agent analysis: {str(e)[:200]}"
    
    def find_market_impact_news(self, limit: int = 10) -> dict:
        """
        Find the most impactful financial news (optimized with caching)
        """
        # Check cache first (2 minute TTL for market impact)
        cache_key = f"market_impact_{limit}"
        if cache_key in _cache:
            if datetime.now() < _cache_ttl.get(cache_key, datetime.now()):
                return _cache[cache_key]
        """
        Find the most impactful financial news using agent approach
        Agent fetches news and analyzes it autonomously
        
        Args:
            limit: Maximum number of news items to analyze
        
        Returns:
            Dict with structured analysis of top market-impacting news
        """
        system_prompt = f"""You are a financial news analysis agent. Your task is to:
1. Fetch top financial headlines using the fetch_top_financial_headlines tool
2. Analyze the news to identify the top {limit} most impactful items
3. Return your analysis as a JSON object with this EXACT structure:

{{
  "news_items": [
    {{
      "rank": 1,
      "title": "News headline or summary",
      "impact_level": "high|medium|low",
      "impact_direction": "positive|negative|neutral",
      "why_it_matters": "Brief explanation of why this news is important",
      "affected_sectors": ["sector1", "sector2"],
      "affected_companies": ["company1", "company2"],
      "trading_insight": "Actionable insight for traders",
      "source": "news source name"
    }}
  ]
}}

CRITICAL: Return ONLY valid JSON. No markdown, no explanations, no code blocks. Just the JSON object.
Ensure you return exactly {limit} news items, properly formatted as valid JSON."""
        
        user_query = f"Find and analyze the top {limit} most impactful financial news items that could significantly affect stock markets. Fetch the latest headlines and return the analysis as a JSON object with the exact structure specified."
        
        try:
            # Optimized: Fetch news first, then analyze (faster than agent loop)
            # Fetch news directly for speed
            news_result = self.news_service.fetch_top_headlines(
                category="business",
                country="us",
                page_size=limit * 2
            )
            
            articles = news_result.get("articles", [])[:limit * 2]
            
            if not articles:
                # Try without category
                news_result = self.news_service.fetch_top_headlines(
                    country="us",
                    page_size=limit * 2
                )
                articles = news_result.get("articles", [])[:limit * 2]
            
            if not articles:
                return {
                    "success": False,
                    "message": "No news articles found.",
                    "news_items": []
                }
            
            # Prepare news summary for Claude
            news_summary = "\n\n".join([
                f"Article {i+1}:\n"
                f"Title: {art.get('title', 'N/A')}\n"
                f"Description: {art.get('description', 'N/A')}\n"
                f"Source: {art.get('source', {}).get('name', 'N/A')}\n"
                f"Published: {art.get('publishedAt', 'N/A')}"
                for i, art in enumerate(articles)
            ])
            
            # Use direct Claude call instead of agent loop for speed
            analysis_prompt = f"""Analyze the following financial news articles and return ONLY a JSON object with this exact structure:

{{
  "news_items": [
    {{
      "rank": 1,
      "title": "News headline",
      "impact_level": "high|medium|low",
      "impact_direction": "positive|negative|neutral",
      "why_it_matters": "Brief explanation",
      "affected_sectors": ["sector1"],
      "affected_companies": ["company1"],
      "trading_insight": "Actionable insight",
      "source": "source name"
    }}
  ]
}}

News Articles:
{news_summary}

Return ONLY valid JSON, no markdown, no explanations. Select the top {limit} most impactful items."""
            
            # Direct API call instead of agent loop (much faster)
            try:
                from anthropic import Anthropic
                client = Anthropic(api_key=settings.CLAUDE_API_KEY)
                response = client.messages.create(
                    model=settings.CLAUDE_MODEL,
                    max_tokens=2048,  # Reduced for speed
                    temperature=0.3,
                    messages=[{"role": "user", "content": analysis_prompt}],
                    system="You are a financial analyst. Return only valid JSON."
                )
                
                agent_response = response.content[0].text if response.content else ""
            except Exception:
                # Fallback to agent if direct call fails
                agent_response = self.claude_ai.run_agent(
                    user_message=user_query,
                    tools=self.tools,
                    tool_executor=execute_tool,
                    system=system_prompt,
                    max_iterations=3,  # Reduced iterations
                    temperature=0.3,
                    max_tokens=2048
                )
            
            # Try to extract structured data from response
            import re
            
            # Remove markdown code blocks if present
            cleaned_response = re.sub(r'```json\s*|\s*```', '', agent_response)
            cleaned_response = cleaned_response.strip()
            
            # Look for JSON in the response
            json_match = re.search(r'\{[^{}]*"news_items"[^{}]*\[[^\]]*\][^{}]*\}', cleaned_response, re.DOTALL)
            if json_match:
                try:
                    parsed_data = json.loads(json_match.group(0))
                    news_items = parsed_data.get("news_items", [])
                    
                    # Validate and clean news items
                    validated_items = []
                    for item in news_items[:limit]:
                        if isinstance(item, dict):
                            validated_items.append({
                                "rank": item.get("rank", len(validated_items) + 1),
                                "title": str(item.get("title", "Unknown"))[:200],
                                "impact_level": item.get("impact_level", "medium").lower(),
                                "impact_direction": item.get("impact_direction", "neutral").lower(),
                                "why_it_matters": str(item.get("why_it_matters", ""))[:500],
                                "affected_sectors": item.get("affected_sectors", []) if isinstance(item.get("affected_sectors"), list) else [],
                                "affected_companies": item.get("affected_companies", []) if isinstance(item.get("affected_companies"), list) else [],
                                "trading_insight": str(item.get("trading_insight", ""))[:500],
                                "source": str(item.get("source", "Unknown"))[:100]
                            })
                    
                    if validated_items:
                        result = {
                            "success": True,
                            "news_items": validated_items
                        }
                        # Cache the result
                        _cache[cache_key] = result
                        _cache_ttl[cache_key] = datetime.now() + timedelta(minutes=2)
                        return result
                except json.JSONDecodeError as e:
                    pass
            
            # Fallback: Try to parse the entire response as JSON
            try:
                parsed_data = json.loads(cleaned_response)
                if "news_items" in parsed_data:
                    news_items = parsed_data.get("news_items", [])[:limit]
                    return {
                        "success": True,
                        "news_items": news_items
                    }
            except json.JSONDecodeError:
                pass
            
            # If no JSON found, fetch news directly and create structured response
            try:
                news_result = self.news_service.fetch_top_headlines(
                    category="business",
                    country="us",
                    page_size=limit
                )
                
                articles = news_result.get("articles", [])[:limit]
                news_items = []
                
                for idx, article in enumerate(articles, 1):
                    news_items.append({
                        "rank": idx,
                        "title": article.get("title", "No title")[:200],
                        "impact_level": "medium",
                        "impact_direction": "neutral",
                        "why_it_matters": article.get("description", "Financial news update")[:500] if article.get("description") else "Market-moving financial news",
                        "affected_sectors": ["General"],
                        "affected_companies": [],
                        "trading_insight": "Monitor market reaction to this news",
                        "source": article.get("source", {}).get("name", "Unknown")[:100]
                    })
                
                result = {
                    "success": True,
                    "news_items": news_items
                }
                # Cache the result
                _cache[cache_key] = result
                _cache_ttl[cache_key] = datetime.now() + timedelta(minutes=2)
                return result
            except Exception:
                pass
            
            # Final fallback
            return {
                "success": False,
                "message": "Unable to parse agent response or fetch news",
                "news_items": []
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error during agent analysis: {str(e)[:200]}",
                "news_items": []
            }


# Create a global agent instance
agent = APIAgent()
