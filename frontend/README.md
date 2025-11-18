# Wise Trade Frontend

A modern, responsive trading dashboard built with React, Vite, and Tailwind CSS.

## Features

- 📊 **Real-time Stock Data**: Live stock quotes and price updates using Alpha Vantage API
- 📈 **Interactive Charts**: Visualize stock price movements with customizable intervals
- 🔍 **Stock Search**: Quick search functionality to find and add stocks to your watchlist
- 📰 **AI News Analysis**: AI-powered analysis of financial news and market impact
- 🎯 **Market Movers**: Track top gainers, losers, and most actively traded stocks
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## Tech Stack

- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Recharts**: Beautiful, composable charts
- **Axios**: HTTP client for API requests
- **Lucide React**: Beautiful icon library

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and visit `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   │   ├── Layout.jsx
│   │   ├── StockCard.jsx
│   │   ├── StockChart.jsx
│   │   └── StockSearch.jsx
│   ├── pages/         # Page components
│   │   ├── Dashboard.jsx
│   │   ├── StockDetail.jsx
│   │   └── NewsAnalysis.jsx
│   ├── services/      # API services
│   │   └── api.js
│   ├── App.jsx        # Main app component
│   ├── main.jsx       # App entry point
│   └── index.css      # Global styles
├── index.html         # HTML template
├── vite.config.js     # Vite configuration
├── tailwind.config.js # Tailwind configuration
└── package.json       # Dependencies
```

## API Integration

The frontend connects to the backend API running on `http://localhost:8000`.

### Stock Endpoints
- `GET /api/stocks/quote/{symbol}` - Get real-time stock quote
- `GET /api/stocks/intraday/{symbol}` - Get intraday price data
- `GET /api/stocks/search` - Search for stocks
- `GET /api/stocks/market-movers` - Get top gainers/losers
- `GET /api/stocks/overview/{symbol}` - Get company overview

### AI News Endpoints
- `GET /api/ai/analyze-news` - Analyze news for a specific query
- `GET /api/ai/market-impact` - Get top market-impacting news

## Features Overview

### Dashboard
- Watchlist with customizable stocks
- Real-time price updates every 30 seconds
- Market movers (gainers, losers, most active)
- Quick stock search and add functionality

### Stock Detail
- Detailed stock information
- Interactive price charts with multiple intervals (1min, 5min, 15min, 30min, 60min)
- Company overview and fundamentals
- Key metrics (PE ratio, market cap, 52-week high/low)

### News Analysis
- AI-powered analysis of market-impacting news
- Custom news search and analysis
- Actionable trading insights
- Sector and company impact assessment

## Customization

### Adding New Routes
Edit `src/App.jsx` to add new routes:

```jsx
<Route path="/your-path" element={<YourComponent />} />
```

### Modifying the Theme
Edit `tailwind.config.js` to customize colors, fonts, and more.

### API Configuration
The API base URL is configured in `vite.config.js` proxy settings.

## Development

### Code Style
- Use functional components with hooks
- Follow ESLint recommendations
- Keep components small and focused
- Use Tailwind utility classes for styling

### State Management
Currently using React's built-in hooks (useState, useEffect). For larger applications, consider adding:
- Redux Toolkit for global state
- React Query for server state management

## Troubleshooting

### Port Already in Use
Change the port in `vite.config.js`:
```js
server: {
  port: 3001, // Change to any available port
}
```

### API Connection Issues
Make sure the backend server is running on `http://localhost:8000`.

### Build Errors
Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

## License

MIT License - feel free to use this project for learning or commercial purposes.

