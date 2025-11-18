# Wise Trade - Application Context

## 🎯 Vision & Purpose

**Wise Trade** is an AI-powered trading consulting platform that analyzes the relationship between financial news and market movements to provide intelligent trading recommendations. The core innovation lies in correlating news sentiment and events with actual market reactions, enabling data-driven trading decisions.

## 🧠 Core Concept

The application bridges the gap between **news events** and **market behavior** by:

1. **Collecting News Data**: Fetching latest financial news from News API covering market events, company announcements, economic indicators, and global financial news
2. **Collecting Market Data**: Fetching real-time market data from Alpha Vantage API including current stock prices, volumes, and technical indicators
3. **Real-time AI Analysis**: Using LLM-powered agent systems to analyze trade information on-the-fly by processing the latest data from both APIs
4. **Trading Recommendations**: Providing actionable trading suggestions based on intelligent analysis of current news-market dynamics without requiring pre-trained models

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Wise Trade Platform                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │  News API    │         │Alpha Vantage │                  │
│  │  Service    │         │   Service    │                  │
│  └──────┬───────┘         └──────┬───────┘                  │
│         │                        │                           │
│         └────────┬───────────────┘                           │
│                  │                                           │
│         ┌────────▼────────┐                                 │
│         │  Data Fetcher   │                                 │
│         │  (Real-time API │                                 │
│         │   Calls)        │                                 │
│         └────────┬────────┘                                 │
│                  │                                           │
│         ┌────────▼────────┐                                 │
│         │  LLM Agent      │                                 │
│         │  System         │                                 │
│         │  - On-the-fly   │                                │
│         │    Analysis     │                                │
│         │  - News-Market  │                                │
│         │    Correlation  │                                │
│         │  - Trading      │                                │
│         │    Insights     │                                │
│         │  - Real-time    │                                │
│         │    Reasoning    │                                │
│         └────────┬────────┘                                 │
│                  │                                           │
│         ┌────────▼────────┐                                 │
│         │  FastAPI Backend│                                 │
│         │  - REST Endpoints│                                │
│         │  - User Auth    │                                 │
│         │  - AI Agent API │                                 │
│         │  - Recommendations│                               │
│         └────────┬────────┘                                 │
│                  │                                           │
│         ┌────────▼────────┐                                 │
│         │   MongoDB       │                                 │
│         │   - User Data   │                                 │
│         │   - Session Data│                                 │
│         │   - Analysis    │                                 │
│         │     History     │                                 │
│         └─────────────────┘                                 │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Data Sources

### 1. News API Integration

**Purpose**: Collect financial news, market events, and economic indicators

**Key Features**:
- Real-time financial news articles
- Company-specific news and announcements
- Economic indicators and policy changes
- Global market news and trends
- News sentiment analysis (positive/negative/neutral)

**Use Cases**:
- Track breaking news that might affect markets
- Monitor company-specific announcements (earnings, mergers, product launches)
- Identify economic indicators (interest rates, employment data, GDP)
- Analyze news sentiment to predict market direction

### 2. Alpha Vantage API Integration

**Purpose**: Collect real-time and historical market data

**Key Endpoints Used**:
- `TIME_SERIES_INTRADAY`: Real-time price movements (1min to 60min intervals)
- `TIME_SERIES_DAILY_ADJUSTED`: Daily OHLCV data with splits/dividends
- `GLOBAL_QUOTE`: Latest real-time quotes (price, change %, volume)
- `SYMBOL_SEARCH`: Search for company tickers
- `CRYPTO_INTRADAY`: Cryptocurrency market data
- `FX_INTRADAY`: Forex market data

**Use Cases**:
- Track price movements after news events
- Calculate technical indicators (RSI, MACD, moving averages)
- Monitor volume spikes correlated with news
- Historical price analysis for pattern recognition

## 🔬 Market-News Correlation Analysis

### How It Works (Real-time LLM Agent System)

1. **Real-time Data Fetching**: When a user requests analysis, the system:
   - Fetches the latest news articles from News API
   - Fetches current market data from Alpha Vantage API
   - No pre-stored data required - everything is fresh

2. **LLM Agent Analysis**: The agent system processes data on-the-fly:
   - **News Analysis**: LLM extracts key information from news articles (events, sentiment, impact)
   - **Market Analysis**: LLM analyzes current market conditions (prices, volumes, trends)
   - **Correlation Reasoning**: LLM reasons about how news events relate to market movements
   - **Trading Insights**: LLM generates actionable trading recommendations based on current context

3. **Agent Capabilities**:
   - Understands financial terminology and market dynamics
   - Identifies significant news events and their potential impact
   - Correlates news sentiment with market data patterns
   - Provides reasoning for trading recommendations
   - Adapts to different market conditions and news types

4. **On-the-Fly Processing**: 
   - No model training required
   - No historical data storage needed
   - Analysis happens in real-time based on latest information
   - Each request gets fresh analysis of current market-news state

### Example Scenarios

- **Earnings Beat**: User requests analysis → System fetches latest earnings news → Fetches current stock price → LLM agent analyzes the news impact and current market state → Provides real-time trading recommendation
- **Regulatory News**: User queries about new regulations → System fetches relevant news → Fetches affected stock prices → LLM agent reasons about regulatory impact → Suggests trading strategy
- **Merger Announcement**: User asks about acquisition news → System collects latest merger news → Fetches current market data → LLM agent analyzes the announcement and market reaction → Generates trading insights

## 🤖 AI/LLM Agent System

### LLM-Powered Agent Architecture

The system uses **Large Language Models (LLMs)** with an **agent framework** to analyze trading information in real-time:

1. **Agent System**:
   - **Multi-Agent Framework**: Specialized agents for different tasks
     - News Analysis Agent: Processes and extracts insights from news articles
     - Market Data Agent: Analyzes current market conditions and trends
     - Correlation Agent: Identifies relationships between news and market movements
     - Trading Advisor Agent: Generates trading recommendations based on combined analysis

2. **Real-time Processing**:
   - Fetches latest data from APIs on-demand
   - No pre-training or model storage required
   - Each analysis is fresh and context-aware
   - LLM reasons about current market-news dynamics

3. **Agent Capabilities**:
   - **Natural Language Understanding**: Processes news articles and market reports
   - **Financial Reasoning**: Understands market dynamics, trading concepts, and financial terminology
   - **Pattern Recognition**: Identifies correlations between news events and market reactions
   - **Recommendation Generation**: Provides actionable trading insights with reasoning
   - **Context Awareness**: Adapts analysis based on current market conditions

4. **On-the-Fly Analysis Flow**:
   ```
   User Request → Fetch Latest News → Fetch Current Market Data → 
   LLM Agent Processes → Generate Insights → Return Recommendations
   ```

### Agent System Benefits

- **No Training Required**: LLMs come pre-trained with financial knowledge
- **Real-time Analysis**: Always uses the most current data
- **Flexible Reasoning**: Can handle novel situations and unexpected news
- **Explainable**: Provides reasoning for recommendations
- **Multi-domain**: Can analyze stocks, crypto, forex, commodities

## 🗂️ Project Structure

```
wise-Trade/
├── app/                          # FastAPI backend application
│   ├── core/                     # Core configuration (database, security, config)
│   ├── models/                   # MongoDB document models
│   ├── repositories/             # Data access layer
│   ├── routers/                  # API route handlers
│   ├── schemas/                  # Pydantic schemas for validation
│   ├── services/                 # Business logic services
│   │   ├── alpha_API_service.py  # Alpha Vantage integration
│   │   ├── auth_service.py       # Authentication logic
│   │   ├── email_service.py      # Email notifications
│   │   └── users_service.py      # User management
│   ├── utils/                    # Utility functions
│   └── main.py                   # FastAPI application entry point
│
├── ml/                           # Legacy ML pipeline (preserved, not actively used)
│   ├── data/                     # Data storage (raw, processed)
│   ├── ml_pipeline/              # ML pipeline components
│   │   ├── ingestion.py         # Data collection
│   │   ├── features.py          # Feature engineering
│   │   ├── training.py          # Model training
│   │   └── evaluation.py       # Model evaluation
│   ├── models/                   # Trained model artifacts
│   ├── notebooks/                # Jupyter notebooks for analysis
│   └── scripts/                  # Utility scripts
│
├── test/                         # Test files
├── Alpha Vantage API documnetation.md  # API documentation
├── CONTEXT.md                    # This file
├── README.md                     # Project README
└── requirements.txt              # Python dependencies
```

## 🔄 Data Flow (Real-time Processing)

### 1. User Request Phase

```
User Request → API Endpoint → Agent System Triggered
```

### 2. Real-time Data Fetching Phase

```
Agent System → News API (Latest Articles) → Raw News Data
Agent System → Alpha Vantage API (Current Market Data) → Raw Market Data
```

### 3. LLM Agent Analysis Phase

```
Raw News Data + Raw Market Data → LLM Agent System → 
  ├─ News Analysis Agent: Extracts key events, sentiment, impact
  ├─ Market Analysis Agent: Analyzes prices, volumes, trends
  ├─ Correlation Agent: Identifies news-market relationships
  └─ Trading Advisor Agent: Generates recommendations
```

### 4. Response Generation Phase

```
Agent Analysis Results → Structured Response → User receives:
  - News insights
  - Market analysis
  - Correlation findings
  - Trading recommendations with reasoning
```

### Key Differences from ML Approach

- **No Data Storage**: Data is fetched fresh for each request
- **No Model Training**: LLM agents use pre-trained knowledge
- **On-the-Fly Processing**: Analysis happens in real-time
- **Context-Aware**: Each analysis considers current market conditions

## 🎯 Key Features (Current & Planned)

### ✅ Implemented
- FastAPI backend with MongoDB
- User authentication (JWT)
- Alpha Vantage API service structure
- Basic data fetching framework

### 🚧 In Progress / Planned
- News API integration
- LLM agent system implementation
- Real-time on-the-fly analysis engine
- Multi-agent framework (News, Market, Correlation, Trading Advisor agents)
- Trading recommendation generation with reasoning
- API endpoints for agent-based analysis
- Dashboard for visualizing real-time analysis results
- Alert system for significant news events
- Agent conversation interface for interactive analysis

## 🔐 Configuration

The application uses environment variables for configuration (see `env_template.txt`):

- **MongoDB**: Connection URI, database name, credentials
- **Alpha Vantage**: API key (free tier: 5 calls/min, 500/day)
- **News API**: API key (to be configured)
- **Security**: JWT secrets, token expiration
- **Email**: SMTP configuration for notifications

## 📈 Use Cases

1. **Day Traders**: Get real-time alerts when news breaks that historically caused significant price movements
2. **Swing Traders**: Identify news patterns that predict multi-day trends
3. **Long-term Investors**: Understand how major events (earnings, policy changes) affect stock prices over weeks/months
4. **Research**: Analyze historical correlations between news types and market reactions

## 🚀 Future Enhancements

- **Multi-source News**: Integrate multiple news sources (Reuters, Bloomberg, etc.)
- **Social Media Sentiment**: Include Twitter/Reddit sentiment analysis
- **Real-time Streaming**: WebSocket support for live updates
- **Portfolio Optimization**: Suggest portfolio adjustments based on news
- **Risk Assessment**: Calculate risk scores for trades based on news volatility
- **Backtesting**: Test strategies against historical news-market data

## 📝 Notes

- **Alpha Vantage Limits**: Free tier has rate limits (5 calls/min, 500/day). Implement request rate limiting and caching where appropriate
- **Data Latency**: Alpha Vantage data is typically delayed by ~1 minute (acceptable for real-time analysis)
- **News API**: Choose appropriate tier based on required news volume and sources
- **LLM API Costs**: Consider token usage and API costs for LLM agent calls. Implement caching for similar queries
- **Real-time Processing**: Each request fetches fresh data - ensure efficient API usage
- **Agent System**: Use appropriate LLM provider (OpenAI, Anthropic, etc.) with proper API key management
- **Scalability**: Consider async processing for multiple agent tasks and API rate limit management
- **ML Folder**: The `ml/` folder is preserved for reference but not actively used in the current LLM-based architecture

---

**Last Updated**: 2024
**Status**: Active Development
**Focus**: LLM Agent System for Real-time News-Market Analysis & Trading Recommendations

