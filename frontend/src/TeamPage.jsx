import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './index.css';

function TeamPage({ league }) {
  const { abbreviation } = useParams();
  const navigate = useNavigate();
  const [teamData, setTeamData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = `http://127.0.0.1:8000/${league}/team/${abbreviation}/catelo-history`;
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        setTeamData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching team data:', error);
        setLoading(false);
      });
  }, [abbreviation, league]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!teamData || !teamData.team) {
    return <div>Team not found</div>;
  }

  const { team, history } = teamData;

  // Prepare chart data
  const chartData = history.map((game, index) => ({
    date: new Date(game.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    catelo: Math.round(game.catelo),
    fullDate: game.date
  }));

  // Determine logo path based on league
  const getLogoPath = () => {
    if (league === 'nba') {
      return `/logos/${team.name.replace(/ /g, '_')}.png`;
    } else {
      return `/logos/${team.abbreviation}.svg`;
    }
  };

  return (
    <>
      <nav />
      <div className="team-page">
        <button onClick={() => navigate(`/${league}`)} className="back-button">
          ← Back to {league.toUpperCase()} Teams
        </button>
        <div className="team-header">
          <img 
            src={getLogoPath()} 
            alt={`${team.name} logo`} 
            className={`team-logo ${league === 'nfl' ? 'nfl-logo-large' : ''}`}
          />
          <div>
            <h1>{team.name}</h1>
            <div className="team-stats-summary">
              <div className="stat-item">
                <span className="stat-label">Current CatElo</span>
                <span className="stat-value">{Math.round(team.current_catelo)}</span>
              </div>
            </div>
          </div>
        </div>

        {history.length > 0 ? (
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
                    color: '#fff'
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
        ) : (
          <div className="no-data">No game history available</div>
        )}

        {history.length > 0 && (
          <div className="game-history">
            <h2>Recent Games</h2>
            <div className="game-list">
              {history.slice(-10).reverse().map((game, index) => (
                <div key={index} className="game-item">
                  <span className="game-date">
                    {new Date(game.date).toLocaleDateString('en-US', { 
                      month: 'short', 
                      day: 'numeric',
                      year: 'numeric'
                    })}
                  </span>
                  <span className="game-opponent">
                    {game.home ? 'vs' : '@'} {game.opponent}
                  </span>
                  <span className="game-score">{game.score}</span>
                  <span className="game-catelo">{Math.round(game.catelo)}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default TeamPage;

