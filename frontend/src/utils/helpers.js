// Utility functions for the app

/**
 * Get company logo URL using UI Avatars
 * @param {string} identifier - Company name or stock symbol
 * @returns {string} Logo URL
 */
export const getCompanyLogo = (identifier) => {
  if (!identifier) return null;
  
  // Use UI Avatars with nice gradient backgrounds
  const colors = ['4F46E5', '7C3AED', 'EC4899', 'F59E0B', '10B981', '3B82F6', 'EF4444'];
  const randomColor = colors[identifier.length % colors.length];
  
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(identifier)}&background=${randomColor}&color=fff&bold=true&size=128`;
};

/**
 * Get company logo with fallback
 * @param {string} identifier - Company name or stock symbol
 * @param {function} onError - Error callback
 * @returns {object} Props for img tag
 */
export const getLogoProps = (identifier, onError) => {
  const logoUrl = getCompanyLogo(identifier);
  
  return {
    src: logoUrl,
    alt: `${identifier} logo`,
    onError: (e) => {
      // Already using UI Avatars which is very reliable
      if (onError) onError(e);
    }
  };
};

/**
 * Format large numbers with K, M, B suffixes
 * @param {number} num - Number to format
 * @returns {string} Formatted number
 */
export const formatNumber = (num) => {
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K';
  return num.toFixed(2);
};

/**
 * Format currency
 * @param {number} value - Value to format
 * @param {string} currency - Currency code (default: USD)
 * @returns {string} Formatted currency
 */
export const formatCurrency = (value, currency = 'USD') => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
};

/**
 * Format date
 * @param {string|Date} date - Date to format
 * @returns {string} Formatted date
 */
export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

/**
 * Format time ago
 * @param {string|Date} date - Date to format
 * @returns {string} Time ago string
 */
export const timeAgo = (date) => {
  const seconds = Math.floor((new Date() - new Date(date)) / 1000);
  
  const intervals = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60,
  };
  
  for (const [unit, secondsInUnit] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / secondsInUnit);
    if (interval >= 1) {
      return `${interval} ${unit}${interval > 1 ? 's' : ''} ago`;
    }
  }
  
  return 'just now';
};

