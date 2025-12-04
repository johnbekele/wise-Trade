from typing import Optional, Dict, Any, List
import json
from functools import lru_cache
from datetime import datetime, timedelta

from app.core.claudeAI import ClaudeAI
from app.services.news_service import NewsService
from app.core.config import settings

news_service = NewsService()
claude_ai = ClaudeAI()

_cache = {}
_cache_ttl = {}


def get_claude_tools() -> List[Dict[str, Any]]:
    return [
        {
            "name": "fetch_top_financial_headlines",
            "description": "Fetch top financial/business headlines that could affect the stock market.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Category of news", "enum": ["business", "technology", "general"]},
                    "page_size": {"type": "integer", "description": "Number of articles to fetch", "minimum": 1, "maximum": 100}
                }
            }
        },
        {
            "name": "search_financial_news",
            "description": "Search for financial news articles based on keywords or topics.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keywords"},
                    "page_size": {"type": "integer", "description": "Number of articles to fetch", "minimum": 1, "maximum": 100}
                },
                "required": ["query"]
            }
        },
        {
            "name": "fetch_stock_news",
            "description": "Fetch news articles specific to a stock ticker symbol.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock ticker symbol"},
                    "page_size": {"type": "integer", "description": "Number of articles to fetch", "minimum": 1, "maximum": 100}
                },
                "required": ["symbol"]
            }
        }
    ]


def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> str:
    try:
        if tool_name == "fetch_top_financial_headlines":
            category = tool_input.get("category", "business")
            page_size = tool_input.get("page_size", 20)
            result = news_service.fetch_top_headlines(category=category, country="us", page_size=page_size)
            if "error" in result:
                return json.dumps({"error": result["error"]})
            articles = result.get("articles", [])
            key_info = news_service.extract_key_info(articles)
            return json.dumps({"status": "success", "total_results": result.get("totalResults", 0), "articles": key_info}, indent=2)
        
        elif tool_name == "search_financial_news":
            query = tool_input.get("query", "")
            page_size = tool_input.get("page_size", 20)
            result = news_service.fetch_financial_news(query=query, page_size=page_size)
            if "error" in result:
                return json.dumps({"error": result["error"]})
            articles = result.get("articles", [])
            key_info = news_service.extract_key_info(articles)
            return json.dumps({"status": "success", "total_results": result.get("totalResults", 0), "query": query, "articles": key_info}, indent=2)
        
        elif tool_name == "fetch_stock_news":
            symbol = tool_input.get("symbol", "").upper()
            page_size = tool_input.get("page_size", 20)
            result = news_service.fetch_stock_specific_news(symbol=symbol, page_size=page_size)
            if "error" in result:
                return json.dumps({"error": result["error"]})
            articles = result.get("articles", [])
            key_info = news_service.extract_key_info(articles)
            return json.dumps({"status": "success", "symbol": symbol, "total_results": result.get("totalResults", 0), "articles": key_info}, indent=2)
        
        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})
    except Exception as e:
        return json.dumps({"error": f"Tool execution failed: {str(e)}"})


class APIAgent:
    def __init__(self):
        self.claude_ai = ClaudeAI()
        self.news_service = NewsService()
        self.tools = get_claude_tools()
    
    def analyze_market_news(self, query: str) -> str:
        # Analyze market news with caching
        cache_key = f"analyze_{query.lower().strip()}"
        if cache_key in _cache:
            if datetime.now() < _cache_ttl.get(cache_key, datetime.now()):
                return _cache[cache_key]
        
        system_prompt = """You are an expert financial analyst AI agent. Your role is to:
1. Use available tools to fetch relevant financial news based on user queries
2. Analyze the fetched news to identify market-moving events
3. Provide comprehensive insights in a structured format

IMPORTANT: Format your response using markdown-style structure:
- Use section headers: "### 1. Most Impactful News Items"
- Use numbered items with bold titles: "1. **News Title**"
- Use bullet points for details: "* Why it matters: ..."

Structure your response with these sections:
1. Most Impactful News Items and Why They Matter
2. Which Companies or Sectors Are Affected
3. Potential Market Impact (high/medium/low) and Direction (positive/negative)
4. Actionable Insights for Traders

Be concise and efficient. Complete your analysis quickly."""
        
        try:
            response = self.claude_ai.run_agent(
                user_message=query,
                tools=self.tools,
                tool_executor=execute_tool,
                system=system_prompt,
                max_iterations=5,
                temperature=0.7,
                max_tokens=2048
            )
            
            if not response or len(response.strip()) == 0:
                return "No analysis could be generated. Please try a different query."
            
            _cache[cache_key] = response
            _cache_ttl[cache_key] = datetime.now() + timedelta(minutes=5)
            return response
        except Exception as e:
            return f"Error during agent analysis: {str(e)[:200]}"
    
    def find_market_impact_news(self, limit: int = 10) -> dict:
        # Find market impact news with caching
        cache_key = f"market_impact_{limit}"
        if cache_key in _cache:
            if datetime.now() < _cache_ttl.get(cache_key, datetime.now()):
                return _cache[cache_key]
       
        system_prompt = f"""You are a financial news analysis agent. Your task is to:
1. Fetch top financial headlines using the fetch_top_financial_headlines tool
2. Analyze the news to identify the top {limit} most impactful items
3. Return your analysis as a JSON object with this EXACT structure:

{{"news_items": [{{"rank": 1, "title": "News headline", "impact_level": "high|medium|low", "impact_direction": "positive|negative|neutral", "why_it_matters": "Brief explanation", "affected_sectors": ["sector1"], "affected_companies": ["company1"], "trading_insight": "Actionable insight", "source": "source name"}}]}}

CRITICAL: Return ONLY valid JSON. No markdown, no explanations. Return exactly {limit} news items."""
        
        user_query = f"Find and analyze the top {limit} most impactful financial news items."
        
        try:
            news_result = self.news_service.fetch_top_headlines(category="business", country="us", page_size=limit * 2)
            articles = news_result.get("articles", [])[:limit * 2]
            
            if not articles:
                news_result = self.news_service.fetch_top_headlines(country="us", page_size=limit * 2)
                articles = news_result.get("articles", [])[:limit * 2]
            
            if not articles:
                return {"success": False, "message": "No news articles found.", "news_items": []}
            
            news_summary = "\n\n".join([
                f"Article {i+1}:\nTitle: {art.get('title', 'N/A')}\nDescription: {art.get('description', 'N/A')}\nSource: {art.get('source', {}).get('name', 'N/A')}"
                for i, art in enumerate(articles)
            ])
            
            analysis_prompt = f"""Analyze the following financial news and return ONLY a JSON object:

{{"news_items": [{{"rank": 1, "title": "News headline", "impact_level": "high|medium|low", "impact_direction": "positive|negative|neutral", "why_it_matters": "Brief explanation", "affected_sectors": ["sector1"], "affected_companies": ["company1"], "trading_insight": "Actionable insight", "source": "source name"}}]}}

News Articles:
{news_summary}

Return ONLY valid JSON. Select the top {limit} most impactful items."""
            
            try:
                from anthropic import Anthropic
                client = Anthropic(api_key=settings.CLAUDE_API_KEY)
                response = client.messages.create(
                    model=settings.CLAUDE_MODEL,
                    max_tokens=2048,
                    temperature=0.3,
                    messages=[{"role": "user", "content": analysis_prompt}],
                    system="You are a financial analyst. Return only valid JSON."
                )
                agent_response = response.content[0].text if response.content else ""
            except Exception:
                agent_response = self.claude_ai.run_agent(
                    user_message=user_query,
                    tools=self.tools,
                    tool_executor=execute_tool,
                    system=system_prompt,
                    max_iterations=3,
                    temperature=0.3,
                    max_tokens=2048
                )
            
            import re
            cleaned_response = re.sub(r'```json\s*|\s*```', '', agent_response).strip()
            
            json_match = re.search(r'\{[^{}]*"news_items"[^{}]*\[[^\]]*\][^{}]*\}', cleaned_response, re.DOTALL)
            if json_match:
                try:
                    parsed_data = json.loads(json_match.group(0))
                    news_items = parsed_data.get("news_items", [])
                    
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
                        result = {"success": True, "news_items": validated_items}
                        _cache[cache_key] = result
                        _cache_ttl[cache_key] = datetime.now() + timedelta(minutes=2)
                        return result
                except json.JSONDecodeError:
                    pass
            
            try:
                parsed_data = json.loads(cleaned_response)
                if "news_items" in parsed_data:
                    return {"success": True, "news_items": parsed_data.get("news_items", [])[:limit]}
            except json.JSONDecodeError:
                pass
            
            try:
                news_result = self.news_service.fetch_top_headlines(category="business", country="us", page_size=limit)
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
                
                result = {"success": True, "news_items": news_items}
                _cache[cache_key] = result
                _cache_ttl[cache_key] = datetime.now() + timedelta(minutes=2)
                return result
            except Exception:
                pass
            
            return {"success": False, "message": "Unable to parse agent response or fetch news", "news_items": []}
        except Exception as e:
            return {"success": False, "message": f"Error during agent analysis: {str(e)[:200]}", "news_items": []}


agent = APIAgent()
