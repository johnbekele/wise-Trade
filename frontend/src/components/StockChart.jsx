import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function StockChart({ data, interval = '5min' }) {
  const timeSeriesKey = `Time Series (${interval})`;
  const timeSeries = data?.data?.[timeSeriesKey] || {};

  const chartData = Object.entries(timeSeries)
    .slice(0, 50)
    .reverse()
    .map(([time, values]) => ({
      time: new Date(time).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
      price: parseFloat(values['4. close']),
      volume: parseInt(values['5. volume'])
    }));

  if (chartData.length === 0) {
    return (
      <div className="card">
        <p className="text-center text-gray-500">No chart data available</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Price Chart ({interval})</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="time" 
            stroke="#6b7280"
            fontSize={12}
          />
          <YAxis 
            stroke="#6b7280"
            fontSize={12}
            domain={['auto', 'auto']}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px'
            }}
          />
          <Line 
            type="monotone" 
            dataKey="price" 
            stroke="#0ea5e9" 
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

