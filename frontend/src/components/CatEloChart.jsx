import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { formatShortDate } from '../lib/format.js';
import './CatEloChart.css';

function CatEloChart({ history }) {
  const chartData = history.map((game) => ({
    date: formatShortDate(game.date),
    catelo: Math.round(game.catelo),
    fullDate: game.date,
  }));

  return (
    <div className="chart-container">
      <h2>CatElo Rating Over Time</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis
            dataKey="date"
            stroke="#fff"
            tick={{ fill: '#fff' }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            stroke="#fff"
            tick={{ fill: '#fff' }}
            domain={['dataMin - 50', 'dataMax + 50']}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1a1a1a',
              border: '1px solid #fff',
              color: '#fff',
            }}
            labelStyle={{ color: '#FFA600' }}
          />
          <Line
            type="monotone"
            dataKey="catelo"
            stroke="#FFA600"
            strokeWidth={2}
            dot={{ fill: '#FFA600', r: 3 }}
            activeDot={{ r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default CatEloChart;
