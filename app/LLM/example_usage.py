"""
Example usage of the APIAgent for analyzing financial news and stock market impact.

This demonstrates how to use the agent to:
1. Fetch financial news
2. Analyze news for stock market impact
3. Find the most impactful news items
"""

from app.LLM.api_agent import agent


def example_analyze_market_news():
    """Example: Analyze general market news"""
    print("=" * 60)
    print("Example 1: Analyzing General Market News")
    print("=" * 60)
    
    query = "Find the latest financial news that could affect stock markets"
    result = agent.analyze_market_news(query)
    print(result)
    print("\n")


def example_find_top_impact_news():
    """Example: Find top impactful news"""
    print("=" * 60)
    print("Example 2: Finding Top Market-Impact News")
    print("=" * 60)
    
    result = agent.find_market_impact_news(limit=5)
    print(result)
    print("\n")


def example_analyze_specific_stock():
    """Example: Analyze news for a specific stock"""
    print("=" * 60)
    print("Example 3: Analyzing News for Specific Stock (AAPL)")
    print("=" * 60)
    
    query = "What news is affecting Apple stock (AAPL)?"
    result = agent.analyze_market_news(query)
    print(result)
    print("\n")


def example_analyze_sector():
    """Example: Analyze news for a specific sector"""
    print("=" * 60)
    print("Example 4: Analyzing Tech Sector News")
    print("=" * 60)
    
    query = "Find news about technology stocks and their potential market impact"
    result = agent.analyze_market_news(query)
    print(result)
    print("\n")


if __name__ == "__main__":
    print("\n🚀 Financial News Analysis Agent - Examples\n")
    
    # Run examples
    try:
        example_analyze_market_news()
        example_find_top_impact_news()
        example_analyze_specific_stock()
        example_analyze_sector()
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()

