# Wise Trade Backend - Comprehensive Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Core Modules](#core-modules)
4. [Models (Data Layer)](#models-data-layer)
5. [Repositories (Data Access Layer)](#repositories-data-access-layer)
6. [Services (Business Logic Layer)](#services-business-logic-layer)
7. [Routers (API Layer)](#routers-api-layer)
8. [Schemas (Data Validation)](#schemas-data-validation)
9. [Special Patterns & Design Decisions](#special-patterns--design-decisions)
10. [Configuration & Environment](#configuration--environment)
11. [Security Implementation](#security-implementation)
12. [Database Architecture](#database-architecture)

---

## Architecture Overview

The Wise Trade backend follows a **layered architecture pattern** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│                      (main.py)                          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Router Layer                         │
│         (API Endpoints - HTTP Request Handlers)        │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Service Layer                         │
│         (Business Logic & Orchestration)                │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                 Repository Layer                         │
│              (Data Access Abstraction)                  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Model Layer                           │
│              (Beanie ODM - MongoDB Documents)           │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  MongoDB Database                       │
└─────────────────────────────────────────────────────────┘
```

### Key Technologies
- **Framework**: FastAPI (async Python web framework)
- **Database**: MongoDB (NoSQL document database)
- **ODM**: Beanie (async MongoDB ODM built on Motor and Pydantic)
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt (via passlib)
- **Email**: aiosmtplib (async SMTP client)
- **AI/LLM**: Google Gemini API (via LangChain)
- **External APIs**: News API, Yahoo Finance (via RapidAPI)

---

## Project Structure

```
wise-Trade/
├── app/
│   ├── core/              # Core configuration and utilities
│   │   ├── config.py      # Environment configuration
│   │   ├── database.py    # Database connection & initialization
│   │   ├── security.py    # JWT & password hashing
│   │   ├── genAI.py       # AI/LLM client wrapper
│   │   └── startup_checks.py  # Health checks on startup
│   │
│   ├── models/             # Database models (Beanie Documents)
│   │   ├── users.py       # User model
│   │   └── auth.py        # AuthToken model
│   │
│   ├── repositories/       # Data access layer
│   │   ├── base_repository.py  # Generic CRUD operations
│   │   ├── users_repository.py # User-specific queries
│   │   └── auth_repository.py  # Token management
│   │
│   ├── services/           # Business logic layer
│   │   ├── users_service.py
│   │   ├── auth_service.py
│   │   ├── email_service.py
│   │   ├── news_service.py
│   │   ├── yahoo_finance_service.py
│   │   └── alpha_API_service.py
│   │
│   ├── routers/           # API endpoints
│   │   ├── users.py       # User management endpoints
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── stocks.py      # Stock market data endpoints
│   │   ├── ai.py          # AI analysis endpoints
│   │   └── test.py        # Testing endpoints
│   │
│   ├── schemas/           # Pydantic models for validation
│   │   ├── user_schema.py
│   │   └── auth_schema.py
│   │
│   ├── LLM/               # AI/LLM integration
│   │   └── api_agent.py   # LangChain agent for news analysis
│   │
│   ├── utils/             # Utility functions
│   │   ├── helpers.py
│   │   └── templates/     # Email templates
│   │
│   └── main.py            # FastAPI application entry point
│
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
└── README.md
```

---

## Core Modules

### 1. `app/core/config.py` - Configuration Management

**Purpose**: Centralized configuration management using environment variables.

**Class**: `Config`
- **Type**: Singleton pattern (instantiated as `settings`)
- **Why**: Single source of truth for all configuration values

**Key Configurations**:
```python
# Database
MONGO_URI              # MongoDB connection string
MONGO_DATABASE         # Database name

# Security
SECRET_KEY             # JWT signing key
REFRESH_SECRET_KEY     # Refresh token signing key
ALGORITHM              # JWT algorithm (default: HS256)

# Email (SMTP)
SMTP_HOST              # SMTP server hostname
SMTP_PORT              # SMTP port (default: 587)
SMTP_USER              # SMTP username
SMTP_PASSWORD          # SMTP password

# External APIs
NEWS_API_KEY           # News API key
RAPIDAPI_KEY           # RapidAPI key for Yahoo Finance
GOOGLE_API_KEY         # Google Gemini API key

# Application
FRONTEND_URL           # Frontend URL for email links
```

**Special Features**:
- Uses `python-dotenv` to load `.env` files
- Provides default values where appropriate
- Type conversions (e.g., `int()` for ports)

---

### 2. `app/core/database.py` - Database Connection

**Purpose**: MongoDB connection management and Beanie initialization.

**Key Functions**:

#### `init_database()`
- **Type**: Async function
- **Purpose**: Initialize MongoDB connection and Beanie ODM
- **Why Async**: Non-blocking database operations for better performance
- **Special Features**:
  - **Connection Pooling**: 
    - `maxPoolSize=50`: Maximum 50 concurrent connections
    - `minPoolSize=10`: Keep 10 connections alive
    - `maxIdleTimeMS=45000`: Close idle connections after 45s
  - **Cloud-Optimized Timeouts**:
    - `serverSelectionTimeoutMS=30000`: 30 seconds (vs 5s default)
    - `connectTimeoutMS=30000`: 30 seconds for initial connection
    - `socketTimeoutMS=30000`: 30 seconds for socket operations
  - **Retry Logic**:
    - `retryWrites=True`: Automatically retry write operations
    - `retryReads=True`: Automatically retry read operations
  - **SSL/TLS Handling**:
    - Primary: Uses `certifi` for certificate validation
    - Fallback: Allows invalid certificates (for development/WSL)

**Why These Settings**:
- **Cloud environments** have higher latency, requiring longer timeouts
- **Connection pooling** reduces connection overhead
- **Retry logic** handles transient network failures

#### `close_db_connection()`
- **Type**: Async function
- **Purpose**: Gracefully close MongoDB connection on application shutdown
- **Why**: Prevents connection leaks and ensures clean shutdown

---

### 3. `app/core/security.py` - Security Manager

**Purpose**: JWT token management, password hashing, and authentication utilities.

**Class**: `SecurityManager`
- **Type**: Singleton (instantiated as `security_manager`)
- **Why**: Single instance ensures consistent security settings

**Key Methods**:

#### Password Management
```python
verify_password(plain_password, hashed_password) -> bool
get_password_hash(plain_password) -> str
```
- **Library**: `passlib` with `bcrypt` scheme
- **Why bcrypt**: Industry-standard, slow hashing prevents brute-force attacks
- **Security**: Automatic salt generation, one-way hashing

#### JWT Token Creation
```python
create_access_token(data, expires_delta) -> str
create_refresh_token(data) -> str
create_verification_token(user_id) -> str
create_reset_token(user_id) -> str
```
- **Library**: `python-jose` (JWT implementation)
- **Algorithm**: HS256 (HMAC-SHA256)
- **Token Types**:
  - **Access Token**: Short-lived (30 minutes default)
  - **Refresh Token**: Long-lived (7 days default)
  - **Verification Token**: 15 minutes (email verification)
  - **Reset Token**: 15 minutes (password reset)

**Why Different Token Types**:
- **Access tokens** are short-lived for security (if stolen, limited damage)
- **Refresh tokens** allow re-authentication without re-login
- **Verification/reset tokens** are single-use, short-lived for security

#### Token Verification
```python
verify_token(token) -> Optional[str]
decode_token(token) -> Dict[str, Any]
```
- **Error Handling**: Returns `None` or error dict instead of raising exceptions
- **Why**: Allows graceful error handling in calling code

#### Special Method: `verify_apple_token()`
- **Purpose**: Verify Apple Sign-In identity tokens
- **Why Special**: Apple uses JWKS (JSON Web Key Set) for public key rotation
- **Process**:
  1. Fetches Apple's public keys from `https://appleid.apple.com/auth/keys`
  2. Finds matching key by `kid` (Key ID)
  3. Constructs RSA public key
  4. Verifies token signature
- **Security**: Uses Apple's rotating public keys (more secure than static keys)

---

### 4. `app/core/genAI.py` - AI/LLM Client

**Purpose**: Wrapper for Google Gemini AI API.

**Class**: `GenAI`
- **Purpose**: Abstracts AI API interactions
- **Library**: `langchain_google_genai` (LangChain integration)

**Key Methods**:

#### `get_llm()`
- **Returns**: `ChatGoogleGenerativeAI` instance
- **Configuration**: Temperature 0.7 (balanced creativity/consistency)
- **Why LangChain**: Provides tool integration and agent capabilities

#### `generate_content_direct(prompt, temperature)`
- **Purpose**: Direct API call bypassing LangChain
- **Why Special**: Avoids LangChain compatibility issues
- **Library**: `google-genai` SDK (direct Google API)
- **Use Case**: When LangChain has version conflicts

**Why Two Methods**:
- LangChain provides agent/tool capabilities
- Direct SDK is more reliable for simple generation

---

### 5. `app/core/startup_checks.py` - Health Checks

**Purpose**: Validate configuration and API connectivity on application startup.

**Key Functions**:

#### `check_api_keys()`
- **Returns**: Dictionary mapping API names to (is_present, message) tuples
- **Why**: Fail fast if critical APIs are misconfigured
- **Checks**:
  - Google AI API key
  - News API key
  - RapidAPI key
  - MongoDB URI
  - Secret keys

#### `test_news_api()`
- **Purpose**: Test News API connectivity
- **Why**: Validates network connectivity and API key validity
- **Features**:
  - SSL certificate handling (with fallback)
  - Detailed error messages for troubleshooting
  - Timeout handling (5 seconds)

#### `test_google_ai_api()`
- **Purpose**: Test Google AI API connectivity
- **Why**: Validates AI service availability
- **Features**:
  - Creates test LLM instance
  - Makes simple API call
  - Handles version compatibility issues

#### `run_startup_checks()`
- **Purpose**: Orchestrates all startup checks
- **Returns**: Boolean (True if all critical checks pass)
- **Why**: Provides clear startup feedback
- **Output**: Formatted console output with status icons

---

## Models (Data Layer)

Models use **Beanie ODM** (Object Document Mapper) which combines:
- **Pydantic**: Data validation and serialization
- **Motor**: Async MongoDB driver
- **Beanie**: ODM layer providing ORM-like interface

### 1. `app/models/users.py` - User Model

**Class**: `User(Document)`
- **Inherits**: `beanie.Document` (MongoDB document)
- **Purpose**: Represents user accounts in the database

**Fields**:
```python
username: str                    # Unique username
first_name: str                 # User's first name
last_name: str                  # User's last name
email: EmailStr                 # Email (validated by Pydantic)
hashed_password: str            # Bcrypt hashed password
is_active: bool = False         # Account active status
is_super_Admin: bool = False    # Admin privileges
is_verified: bool = False       # Email verification status
reset_token: Optional[str]      # Password reset token
created_at: datetime            # Account creation timestamp
updated_at: datetime            # Last update timestamp
```

**Special Methods**:

#### `to_dict_with_id()`
- **Purpose**: Convert Beanie document to dictionary with string ID
- **Why Special**: Beanie stores `_id` as `ObjectId`, but API needs string
- **Process**: Converts `ObjectId` to string for JSON serialization

**Settings**:
```python
class Settings:
    name = "users"  # MongoDB collection name
```

**Why Beanie**:
- **Type Safety**: Pydantic validation ensures data integrity
- **Async**: Non-blocking database operations
- **Automatic Serialization**: Converts to/from JSON automatically
- **Query Builder**: MongoDB queries with Python syntax

---

### 2. `app/models/auth.py` - AuthToken Model

**Class**: `AuthToken(Document)`
- **Purpose**: Stores JWT tokens for verification, password reset, etc.

**Fields**:
```python
token: str                                    # JWT token string
token_type: Literal["access", "refresh",      # Token type (enforced)
                    "password_reset",
                    "email_verification"]
user_id: str                                  # Associated user ID
created_at: datetime                          # Token creation time
expires_at: datetime                          # Token expiration time
```

**Why Store Tokens**:
- **Verification Tokens**: Must be stored to verify email/password reset
- **Token Revocation**: Can invalidate tokens before expiration
- **Audit Trail**: Track token usage and expiration

**Token Types**:
- **access**: Short-lived authentication tokens
- **refresh**: Long-lived token refresh tokens
- **password_reset**: Single-use password reset tokens
- **email_verification**: Email verification tokens

---

## Repositories (Data Access Layer)

Repositories abstract database operations, providing a clean interface for services.

### 1. `app/repositories/base_repository.py` - Generic Repository

**Class**: `BaseRepository[DocumentType]`
- **Type**: Generic class (Python generics)
- **Purpose**: Provides common CRUD operations for all models
- **Why Generic**: DRY principle - avoid code duplication

**Type Variable**:
```python
DocumentType = TypeVar("DocumentType", bound=Document)
```
- **Why**: Ensures only Beanie Documents can be used
- **Benefit**: Type safety and IDE autocomplete

**Key Methods**:

#### `create(data: Dict) -> DocumentType`
- **Purpose**: Insert new document
- **Error Handling**: Catches `DuplicateKeyError` for unique constraints
- **Why Async**: Non-blocking database operations

#### `find_by_id(id: str) -> Optional[DocumentType]`
- **Purpose**: Find document by MongoDB `_id`
- **Special**: Converts string ID to `PydanticObjectId`
- **Why Optional**: Document may not exist

#### `find_one(query: dict) -> Optional[DocumentType]`
- **Purpose**: Find document by custom query
- **Flexibility**: Allows complex MongoDB queries

#### `update(id: str, data: dict) -> Optional[DocumentType]`
- **Purpose**: Update document fields
- **Process**: 
  1. Find document
  2. Update fields using `setattr()`
  3. Save document
- **Why This Approach**: Preserves Beanie document methods

#### `delete(id: str) -> Optional[DocumentType]`
- **Purpose**: Delete document
- **Returns**: Deleted document (for confirmation)

#### `find_all(skip, limit) -> List[DocumentType]`
- **Purpose**: Paginated document retrieval
- **Why Pagination**: Prevents loading entire collections into memory

**Why Repository Pattern**:
- **Separation of Concerns**: Business logic doesn't know about database
- **Testability**: Can mock repositories for unit tests
- **Flexibility**: Can swap database implementations
- **Reusability**: Common operations in one place

---

### 2. `app/repositories/users_repository.py` - User Repository

**Class**: `UsersRepository(BaseRepository)`
- **Inherits**: `BaseRepository[User]`
- **Purpose**: User-specific database operations

**Key Methods**:

#### `create_user(user_data, hashed_password) -> UserRead`
- **Purpose**: Create user with password hashing
- **Why Special**: Combines user creation with password hashing
- **Returns**: `UserRead` schema (not model) for API response

#### `find_by_email(email) -> Optional[UserRead]`
- **Purpose**: Find user by email (for login)
- **Why Special**: Email is indexed for fast lookups
- **Returns**: `UserRead` schema

#### `find_by_username(username) -> Optional[UserRead]`
- **Purpose**: Find user by username (for login)
- **Why Special**: Username is indexed for fast lookups

#### `get_user_by_id(user_id) -> UserRead`
- **Purpose**: Alias for `find_by_id` with schema conversion
- **Why**: Consistent API - always returns `UserRead`

#### `get_all_users(skip, limit) -> List[UserRead]`
- **Purpose**: Paginated user list
- **Why Pagination**: Prevents loading all users at once

#### `update_user(user_id, user_data) -> UserRead`
- **Purpose**: Update user with validation
- **Uses**: `exclude_unset=True` to only update provided fields

#### `delete_user(user_id) -> Optional[dict]`
- **Purpose**: Delete user
- **Returns**: Confirmation message with user_id

**Why Separate Repository**:
- **Domain-Specific Queries**: User-specific search methods
- **Schema Conversion**: Converts models to API schemas
- **Business Logic**: User creation includes password hashing

---

### 3. `app/repositories/auth_repository.py` - Auth Repository

**Class**: `AuthRepository(BaseRepository)`
- **Inherits**: `BaseRepository[AuthToken]`
- **Purpose**: Token management operations

**Key Methods**:

#### `create_token(token, user_id, token_type) -> AuthToken`
- **Purpose**: Create and store token
- **Special**: Automatically sets expiration (15 minutes)
- **Why Store**: Enables token revocation and verification

#### `find_by_token(token) -> Optional[AuthTokenRead]`
- **Purpose**: Find token by token string
- **Use Case**: Verify email verification tokens, password reset tokens

**Why Separate Repository**:
- **Token-Specific Logic**: Token expiration, type validation
- **Security**: Centralized token management

---

## Services (Business Logic Layer)

Services contain business logic and orchestrate multiple repositories.

### 1. `app/services/users_service.py` - User Service

**Class**: `UserService`
- **Purpose**: User management business logic
- **Dependencies**: 
  - `UsersRepository`
  - `AuthRepository`
  - `EmailService`
  - `AuthService`

**Key Methods**:

#### `create_user(user_data, background_tasks) -> UserRead`
- **Purpose**: Complete user registration flow
- **Process**:
  1. Check if user/username exists
  2. Hash password
  3. Create user in database
  4. Generate verification token
  5. Store token in database
  6. Send verification email (background task)
- **Why Background Tasks**: Email sending is slow; don't block response
- **Error Handling**: User creation succeeds even if email fails

**Why Service Layer**:
- **Orchestration**: Coordinates multiple repositories
- **Business Rules**: Enforces validation (e.g., unique email)
- **Transaction Logic**: Ensures data consistency

#### `get_all_users() -> List[UserRead]`
- **Purpose**: Retrieve all users
- **Delegates**: To repository

#### `get_user_by_id(user_id) -> UserRead`
- **Purpose**: Get single user
- **Delegates**: To repository

#### `update_user(user_id, user_data) -> UserRead`
- **Purpose**: Update user information
- **Delegates**: To repository

#### `delete_user(user_id) -> UserRead`
- **Purpose**: Delete user
- **Special**: Returns user data before deletion (for confirmation)
- **Fallback**: Direct MongoDB query if Beanie fails

---

### 2. `app/services/auth_service.py` - Authentication Service

**Class**: `AuthService`
- **Purpose**: Authentication and authorization logic
- **Dependencies**:
  - `AuthRepository`
  - `UsersRepository`
  - `EmailService`
  - `SecurityManager`

**Key Methods**:

#### `create_token(token, payload, token_type) -> str`
- **Purpose**: Create JWT token based on type
- **Token Types**:
  - `email_verification`: 15-minute verification token
  - `password_reset`: 15-minute reset token
  - `refresh`: 7-day refresh token
  - `access`: 30-minute access token
- **Why Different Types**: Different expiration and use cases

#### `login(username, password) -> LoginResponse`
- **Purpose**: Authenticate user
- **Process**:
  1. Find user by email or username
  2. Verify user is active and verified
  3. Verify password
  4. Generate access token
  5. Return token and user info
- **Security**: Never reveals if username or password is wrong (prevents enumeration)

#### `send_email_verification(user_id, background_tasks) -> str`
- **Purpose**: Send email verification link
- **Process**:
  1. Get user by ID
  2. Generate verification token
  3. Store token
  4. Create verification link
  5. Send email (background task)
- **Why Background**: Email sending is slow

#### `verify_email(token) -> Optional[str]`
- **Purpose**: Verify email using token
- **Process**:
  1. Verify JWT token structure
  2. Check token exists in database
  3. Verify token type
  4. Get user
  5. Check if already verified
  6. Mark user as verified and active
  7. Delete token (optional)
- **Error Handling**: Returns descriptive error messages

#### `find_by_token(token) -> Optional[UserRead]`
- **Purpose**: Get user from JWT token
- **Use Case**: Protected routes (get current user)

---

### 3. `app/services/email_service.py` - Email Service

**Class**: `EmailService`
- **Purpose**: Send emails via SMTP
- **Library**: `aiosmtplib` (async SMTP)

**Key Methods**:

#### `get_template(template_name) -> str`
- **Purpose**: Load HTML email template
- **Location**: `app/utils/templates/{template_name}.html`
- **Why Templates**: Reusable, maintainable email designs

#### `send_email(to_email, subject, body) -> None`
- **Purpose**: Send HTML email
- **Process**:
  1. Validate SMTP configuration
  2. Create MIMEText message
  3. Connect to SMTP server
  4. Authenticate
  5. Send message
  6. Close connection
- **Special Features**:
  - **Timeouts**: 30-second timeout for all operations
  - **Error Handling**: Proper connection cleanup on failure
  - **SSL/TLS**: Uses `certifi` for certificate validation
- **Why Async**: Non-blocking email sending

**Why Separate Service**:
- **Reusability**: Multiple services need email
- **Abstraction**: Hides SMTP implementation details
- **Maintainability**: Email logic in one place

---

### 4. `app/services/news_service.py` - News Service

**Class**: `NewsService`
- **Purpose**: Fetch financial news from News API
- **Library**: `requests` (HTTP client)

**Key Methods**:

#### `fetch_top_headlines(category, country, query, page_size) -> Dict`
- **Purpose**: Get top news headlines
- **API**: News API `/top-headlines` endpoint
- **Features**:
  - SSL verification with fallback
  - Error handling
  - Pagination support

#### `fetch_everything(query, sort_by, language, page_size, from_date, to_date) -> Dict`
- **Purpose**: Search all news articles
- **API**: News API `/everything` endpoint
- **Features**: Date range filtering, sorting

#### `fetch_financial_news(query, page_size) -> Dict`
- **Purpose**: Fetch business/financial news
- **Special**: Filters for financial keywords

#### `fetch_stock_specific_news(symbol, page_size) -> Dict`
- **Purpose**: Get news for specific stock
- **Special**: Searches for stock symbol in news

#### `extract_key_info(articles) -> List[Dict]`
- **Purpose**: Extract relevant fields from articles
- **Why**: Reduces data size, focuses on important info

**Why Separate Service**:
- **API Abstraction**: Hides News API implementation
- **Error Handling**: Centralized error management
- **Reusability**: Used by AI agent and other services

---

### 5. `app/services/yahoo_finance_service.py` - Stock Data Service

**Class**: `YahooFinanceService`
- **Purpose**: Fetch stock market data from Yahoo Finance (via RapidAPI)
- **Library**: `requests`

**Key Methods**:

#### `get_quote(symbol) -> Dict`
- **Purpose**: Get real-time stock quote
- **Special**: Falls back to mock data if API fails/rate-limited
- **Why Mock Data**: Prevents API failures from breaking application
- **Data**: Price, volume, change, high/low, etc.

#### `search_symbol(query) -> Dict`
- **Purpose**: Search for stocks by symbol or name
- **Returns**: List of matching stocks

#### `get_market_movers() -> Dict`
- **Purpose**: Get top gainers, losers, most active stocks
- **Returns**: Three lists of stocks

**Why Mock Data Fallback**:
- **Rate Limiting**: Free API tiers have limits
- **Reliability**: Application continues working during API issues
- **Development**: Works without API keys

---

## Routers (API Layer)

Routers define HTTP endpoints and handle request/response.

### 1. `app/routers/users.py` - User Endpoints

**Router**: `APIRouter()`
- **Prefix**: `/api/users`
- **Tags**: `["users"]` (for API documentation)

**Endpoints**:

#### `POST /api/users/signup`
- **Purpose**: User registration
- **Request**: `UserCreate` schema
- **Response**: `UserRead` schema
- **Special**: Uses `BackgroundTasks` for email sending
- **Why Background**: Email doesn't block response

#### `GET /api/users/`
- **Purpose**: List all users
- **Response**: `List[UserRead]`
- **Use Case**: Admin panel

#### `GET /api/users/get-user/{user_id}`
- **Purpose**: Get single user
- **Response**: `UserRead`

#### `DELETE /api/users/{user_id}`
- **Purpose**: Delete user
- **Response**: `UserRead` (deleted user data)

**Dependency Injection**:
```python
user_service: UserService = Depends(get_user_service)
```
- **Why**: FastAPI dependency injection
- **Benefit**: Easy testing (can mock service)

---

### 2. `app/routers/auth.py` - Authentication Endpoints

**Router**: `APIRouter()`
- **Prefix**: `/api/auth`
- **Tags**: `["auth"]`

**Endpoints**:

#### `POST /api/auth/login`
- **Purpose**: User authentication
- **Request**: `LoginRequest` (username, password)
- **Response**: `LoginResponse` (token, user info)
- **Security**: Returns 401 for invalid credentials

#### `GET /api/auth/verify-email?token=...`
- **Purpose**: Verify email address
- **Query Parameter**: `token` (JWT verification token)
- **Response**: Success/error message
- **Error Handling**: Proper HTTP status codes (400, 404, 500)

#### `POST /api/auth/resend-email-verification/{user_id}`
- **Purpose**: Resend verification email
- **Special**: Uses `BackgroundTasks` for email

#### `GET /api/auth/me`
- **Purpose**: Get current user from token
- **Security**: Requires Bearer token
- **Uses**: `HTTPBearer` scheme
- **Response**: `UserRead`

**Security**:
- **Bearer Token**: Standard JWT authentication
- **Error Handling**: Never reveals if user exists (security)

---

### 3. `app/routers/stocks.py` - Stock Market Endpoints

**Router**: `APIRouter()`
- **Prefix**: `/api/stocks`
- **Tags**: `["stocks"]`

**Endpoints**:

#### `GET /api/stocks/quote/{symbol}`
- **Purpose**: Get real-time stock quote
- **Response**: Formatted quote data

#### `GET /api/stocks/search?keywords=...`
- **Purpose**: Search for stocks
- **Query Parameter**: `keywords`
- **Response**: List of matching stocks

#### `GET /api/stocks/market-movers`
- **Purpose**: Get top gainers, losers, most active
- **Response**: Three lists of stocks

#### `GET /api/stocks/profile/{symbol}`
- **Purpose**: Get company profile
- **Response**: Company information

#### `GET /api/stocks/candles/{symbol}`
- **Purpose**: Get historical price data (candlesticks)
- **Note**: Currently returns empty (API limitation)

**Data Transformation**:
- **Why**: Yahoo Finance API format differs from frontend expectations
- **Process**: Transforms API response to consistent format

---

### 4. `app/routers/ai.py` - AI Analysis Endpoints

**Router**: `APIRouter()`
- **Prefix**: `/api/ai`
- **Tags**: `["ai"]`

**Endpoints**:

#### `GET /api/ai/analyze-news/{query}`
#### `GET /api/ai/analyze-news?query=...`
#### `POST /api/ai/analyze-news`
- **Purpose**: Analyze financial news for market impact
- **Request**: Query string (company, topic, etc.)
- **Response**: AI analysis of news
- **Why Multiple Methods**: Flexibility for different use cases

#### `GET /api/ai/market-impact?limit=10`
- **Purpose**: Get most impactful financial news
- **Response**: List of news articles with impact analysis

**AI Integration**:
- **Uses**: `APIAgent` from `app/LLM/api_agent.py`
- **Process**: Fetches news → AI analyzes → Returns insights

---

## Schemas (Data Validation)

Schemas use **Pydantic** for validation and serialization.

### 1. `app/schemas/user_schema.py`

**Schemas**:

#### `UserCreate`
- **Purpose**: User registration input
- **Fields**: username, first_name, last_name, email, password
- **Validation**: Email format, required fields

#### `UserRead`
- **Purpose**: User data returned by API
- **Fields**: All user fields including `id`
- **Why Separate**: Excludes password, includes computed fields

#### `UserUpdate`
- **Purpose**: Partial user updates
- **Fields**: All optional (Pydantic `Optional`)
- **Why Optional**: Only update provided fields

#### `UserDeleteResponse`
- **Purpose**: Delete confirmation
- **Fields**: message, user_id

**Why Pydantic**:
- **Validation**: Automatic type checking
- **Serialization**: Converts to/from JSON
- **Documentation**: Auto-generates API docs

---

### 2. `app/schemas/auth_schema.py`

**Schemas**:

#### `LoginRequest`
- **Purpose**: Login input
- **Fields**: username, password

#### `LoginResponse`
- **Purpose**: Login output
- **Fields**: token, token_type, user

#### `TokenPayload`
- **Purpose**: JWT token payload
- **Fields**: sub (user ID), first_name, last_name, email, exp

#### `AuthTokenRead`
- **Purpose**: Token data
- **Fields**: token, token_type, user_id, created_at, expires_at

#### `EmailVerificationResponse`
- **Purpose**: Email verification response
- **Fields**: message

**Literal Types**:
```python
token_type: Literal["access", "refresh", "password_reset", "email_verification"]
```
- **Why**: Enforces specific values (type safety)

---

## Special Patterns & Design Decisions

### 1. Repository Pattern

**Why**:
- **Separation of Concerns**: Business logic doesn't know about database
- **Testability**: Can mock repositories
- **Flexibility**: Can swap database implementations

**Implementation**:
- Generic `BaseRepository` for common operations
- Specific repositories for domain logic

---

### 2. Service Layer Pattern

**Why**:
- **Business Logic**: Centralized business rules
- **Orchestration**: Coordinates multiple repositories
- **Transaction Management**: Ensures data consistency

**Example**: `UserService.create_user()` orchestrates:
- User repository (create user)
- Auth repository (create token)
- Email service (send email)

---

### 3. Dependency Injection

**FastAPI Dependency System**:
```python
def get_user_service() -> UserService:
    return UserService()

@router.post("/signup")
async def create_user(
    user_service: UserService = Depends(get_user_service)
):
    ...
```

**Why**:
- **Testability**: Easy to mock dependencies
- **Lifetime Management**: FastAPI manages object lifecycle
- **Type Safety**: IDE autocomplete and type checking

---

### 4. Background Tasks

**FastAPI BackgroundTasks**:
```python
@router.post("/signup")
async def create_user(
    background_tasks: BackgroundTasks,
    ...
):
    background_tasks.add_task(send_email, ...)
```

**Why**:
- **Performance**: Don't block response for slow operations
- **User Experience**: Fast API responses
- **Reliability**: Email failures don't break user creation

---

### 5. Async/Await Pattern

**Why Async**:
- **Non-Blocking**: Can handle multiple requests concurrently
- **Performance**: Better resource utilization
- **Scalability**: Handles more concurrent users

**Where Used**:
- All database operations
- Email sending
- External API calls
- All route handlers

---

### 6. Error Handling Strategy

**Layers**:
1. **Repository**: Returns `None` or raises exceptions
2. **Service**: Handles business logic errors
3. **Router**: Converts to HTTP status codes

**Example**:
```python
# Repository
async def find_by_id(id: str) -> Optional[Document]:
    return await self.model.find_one({"_id": id})

# Service
user = await repository.find_by_id(id)
if not user:
    raise HTTPException(status_code=404, detail="User not found")

# Router
try:
    return await service.get_user(id)
except HTTPException:
    raise  # Re-raise HTTP exceptions
```

---

### 7. Configuration Management

**Environment Variables**:
- All sensitive data in `.env` file
- Loaded via `python-dotenv`
- Centralized in `Config` class

**Why**:
- **Security**: Secrets not in code
- **Flexibility**: Different configs for dev/prod
- **12-Factor App**: Follows best practices

---

### 8. Database Connection Pooling

**Settings**:
- `maxPoolSize=50`: Maximum connections
- `minPoolSize=10`: Minimum connections
- `maxIdleTimeMS=45000`: Close idle connections

**Why**:
- **Performance**: Reuse connections (faster)
- **Resource Management**: Limits connection usage
- **Cloud Optimization**: Handles variable load

---

### 9. Token Management Strategy

**Multiple Token Types**:
- **Access**: Short-lived (30 min)
- **Refresh**: Long-lived (7 days)
- **Verification**: Single-use (15 min)
- **Reset**: Single-use (15 min)

**Why**:
- **Security**: Short-lived tokens reduce risk
- **User Experience**: Refresh tokens avoid frequent logins
- **Single-Use**: Verification/reset tokens prevent reuse

---

### 10. Email Template System

**Location**: `app/utils/templates/`
- HTML templates with placeholders
- Loaded dynamically
- Placeholders replaced with actual data

**Why**:
- **Maintainability**: Separate design from code
- **Reusability**: Same template for multiple emails
- **Consistency**: Uniform email design

---

## Configuration & Environment

### Environment Variables

**Required**:
```bash
MONGO_URI=mongodb://...
MONGO_DATABASE=wise
SECRET_KEY=...
REFRESH_SECRET_KEY=...
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
FRONTEND_URL=http://localhost:3000
```

**Optional**:
```bash
NEWS_API_KEY=...
RAPIDAPI_KEY=...
GOOGLE_API_KEY=...
```

### Configuration Loading

**Process**:
1. `.env` file loaded by `python-dotenv`
2. `Config` class reads environment variables
3. Default values provided where appropriate
4. Type conversions applied (e.g., `int()` for ports)

---

## Security Implementation

### Password Security

**Hashing**:
- **Algorithm**: bcrypt
- **Library**: passlib
- **Why**: Industry standard, slow hashing prevents brute-force

**Process**:
1. User provides plain password
2. `SecurityManager.get_password_hash()` hashes it
3. Hashed password stored in database
4. Login: `SecurityManager.verify_password()` compares

### JWT Security

**Token Structure**:
```
Header.Payload.Signature
```

**Payload**:
- `sub`: User ID
- `exp`: Expiration timestamp
- Additional: first_name, last_name, email

**Signing**:
- **Algorithm**: HS256 (HMAC-SHA256)
- **Secret**: `SECRET_KEY` (never exposed)

**Validation**:
- Signature verification
- Expiration checking
- Token type validation

### Email Verification

**Flow**:
1. User registers
2. Verification token generated (JWT)
3. Token stored in database
4. Email sent with verification link
5. User clicks link
6. Token verified
7. User marked as verified

**Security**:
- Token expires in 15 minutes
- Token stored in database (can be revoked)
- Single-use token (deleted after verification)

### CORS Configuration

**Settings**:
```python
allow_origins=["http://localhost:3000", "https://wise-trade-client.vercel.app"]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

**Why**:
- **Security**: Prevents unauthorized domains
- **Flexibility**: Supports multiple frontend URLs

---

## Database Architecture

### MongoDB Structure

**Collections**:
- `users`: User accounts
- `auth_tokens`: JWT tokens

### Document Structure

**User Document**:
```json
{
  "_id": ObjectId("..."),
  "username": "johndoe",
  "email": "john@example.com",
  "hashed_password": "$2b$12$...",
  "is_active": true,
  "is_verified": true,
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

**AuthToken Document**:
```json
{
  "_id": ObjectId("..."),
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "email_verification",
  "user_id": "507f1f77bcf86cd799439011",
  "created_at": ISODate("..."),
  "expires_at": ISODate("...")
}
```

### Indexing

**Automatic Indexes** (Beanie):
- `_id`: Primary key (automatic)
- Email: Unique index (for fast lookups)
- Username: Unique index (for fast lookups)

**Why Indexes**:
- **Performance**: Fast queries
- **Uniqueness**: Enforce constraints

---

## Summary

### Architecture Principles

1. **Separation of Concerns**: Each layer has specific responsibility
2. **Dependency Injection**: Loose coupling, easy testing
3. **Async/Await**: Non-blocking operations for performance
4. **Type Safety**: Pydantic validation throughout
5. **Error Handling**: Graceful error handling at each layer
6. **Security First**: Password hashing, JWT, email verification
7. **Scalability**: Connection pooling, background tasks
8. **Maintainability**: Clear structure, documentation

### Key Design Decisions

- **Beanie ODM**: Type-safe, async MongoDB operations
- **Repository Pattern**: Abstract data access
- **Service Layer**: Business logic separation
- **Background Tasks**: Non-blocking email sending
- **Mock Data Fallback**: Resilience to API failures
- **Cloud-Optimized**: Longer timeouts, connection pooling

This architecture provides a solid foundation for a scalable, maintainable, and secure backend application.

