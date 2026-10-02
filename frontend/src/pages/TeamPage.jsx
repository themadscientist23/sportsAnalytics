import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { API_URL } from '../lib/api.js';
import { LEAGUES } from '../lib/leagues.js';
import TeamHeader from '../components/TeamHeader.jsx';
import CatEloChart from '../components/CatEloChart.jsx';
import RecentGames from '../components/RecentGames.jsx';
import './TeamPage.css';

function TeamPage({ league }) {
  const { abbreviation } = useParams();
  const navigate = useNavigate();
  const [teamData, setTeamData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_URL}/${league}/seasons`)
      .then((response) => response.json())
      .then((seasons) =>
        fetch(
          `${API_URL}/${league}/seasons/${seasons[seasons.length - 1]}/teams/${abbreviation}`,
        ),
      )
      .then((response) => response.json())
      .then((data) => {
        setTeamData(data);
        setLoading(false);
      })
      .catch((error) => {
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

  return (
    <div className="team-page">
      <button onClick={() => navigate(`/${league}`)} className="back-button">
        ← Back to {LEAGUES[league].title}
      </button>
      <TeamHeader league={league} team={team} />
      {history.length > 0 ? (
        <>
          <CatEloChart history={history} />
          <RecentGames history={history} />
        </>
      ) : (
        <div className="no-data">No game history available</div>
      )}
    </div>
  );
}

export default TeamPage;
