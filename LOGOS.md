# Company Logo Integration

The app uses **Brandfetch** to display company logos throughout the interface.

## Setup

1. **Get your Brandfetch API Key:**
   - Visit: https://brandfetch.com/
   - Sign up for a free account
   - Get your API key (Client ID)

2. **Add to environment variables:**

Create a `.env` file in the `frontend` directory:

```bash
# frontend/.env
VITE_LOGO_API_KEY=your_brandfetch_client_id_here
```

## Features

- ✅ **Stock Cards** - Company logos on dashboard
- ✅ **News Analysis** - Logos for affected companies
- ✅ **Automatic Fallback** - Uses UI Avatars if logo fails to load
- ✅ **Symbol Mapping** - Converts stock symbols to company domains

## How It Works

The `helpers.js` utility file provides:

### `getCompanyLogo(identifier)`
Returns the logo URL for a given company identifier (stock symbol or domain).

### `getLogoProps(identifier)`
Returns props for `<img>` tag with automatic fallback handling.

### Example Usage:

```jsx
import { getLogoProps } from '../utils/helpers';

// In your component
<img {...getLogoProps('AAPL')} className="w-12 h-12" />
```

## Symbol to Domain Mapping

The utility automatically maps common stock symbols to their domains:

- `AAPL` → `apple.com`
- `GOOGL` → `google.com`
- `MSFT` → `microsoft.com`
- `TSLA` → `tesla.com`
- ...and 30+ more

For unlisted symbols, it defaults to `{symbol}.com`.

## Fallback System

If the Brandfetch logo fails to load, the app automatically falls back to **UI Avatars**:
- Creates a colorful avatar with the company's initials
- Ensures logos always display, even without API key

## Without API Key

The app works without a Brandfetch API key:
- Uses UI Avatars for all logos
- Still looks professional with colored avatars

## Adding More Symbol Mappings

Edit `frontend/src/utils/helpers.js` and add to the `symbolToDomain` object:

```javascript
const symbolToDomain = {
  'AAPL': 'apple.com',
  'YOUR_SYMBOL': 'company-domain.com',
  // ... add more
};
```

## API Information

- **Service**: Brandfetch
- **Endpoint**: `https://cdn.brandfetch.io/{domain}?c={clientId}`
- **Free Tier**: Yes, with limits
- **Documentation**: https://brandfetch.com/docs

## Troubleshooting

### Logos not loading?
1. Check your API key in `.env`
2. Make sure it's `VITE_LOGO_API_KEY` (with `VITE_` prefix)
3. Restart the dev server after adding the key
4. Check browser console for errors

### Wrong logo showing?
- Check the symbol to domain mapping in `helpers.js`
- Add the correct mapping for that symbol

### All logos are colored avatars?
- No API key is set (this is normal)
- Or Brandfetch is rate-limiting (free tier limits)

