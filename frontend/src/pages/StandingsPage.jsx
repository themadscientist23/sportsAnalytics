import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../lib/api.js';
import { LEAGUES, logoUrl } from '../lib/leagues.js';
import { formatCatelo } from '../lib/format.js';
import './StandingsPage.css';

const withStats = (team, hasTies) => {
  const games = team.wins + team.losses + (hasTies ? team.ties : 0);
  return {
    ...team,
    winPercentage: games > 0 ? (team.wins / games) * 100 : 0,
    pointsForPerGame: games > 0 ? team.points_for / games : 0,
    pointsAgainstPerGame: games > 0 ? team.points_against / games : 0,
    pointsDifferential: games > 0 ? (team.points_for - team.points_against) / games : 0,
  };
};

function StandingsPage({ league }) {
  const { title, hasTies } = LEAGUES[league];
  const navigate = useNavigate();
  const [teams, setTeams] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: 'catelo', direction: 'descending' });

  useEffect(() => {
    fetch(`${API_URL}/${league}/seasons`)
      .then(response => response.json())
      .then(seasons => fetch(`${API_URL}/${league}/seasons/${seasons[seasons.length - 1]}/teams`))
      .then(response => response.json())
      .then(data => setTeams(data.map(team => withStats(team, hasTies))))
      .catch(error => console.error('Error fetching standings:', error));
  }, [league, hasTies]);

  const sortBy = (key) => {
    const direction = sortConfig.key === key && sortConfig.direction === 'descending' ? 'ascending' : 'descending';
    setSortConfig({ key, direction });
  };

  const sortedTeams = [...teams].sort((a, b) => {
    const { key, direction } = sortConfig;
    if (direction === 'ascending') {
      return a[key] > b[key] ? 1 : -1;
    } else {
      return a[key] < b[key] ? 1 : -1;
    }
  });

  const sortableHeader = (key, label) => (
    <th onClick={() => sortBy(key)} className={`sortable ${sortConfig.key === key ? (sortConfig.direction === "ascending" ? "sort-asc" : "sort-desc") : ""}`}>
      {label}
    </th>
  );

  return (
    <>
      <h1>{title}</h1>
      <div className="standings">
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Team</th>
                {sortableHeader("catelo", "CatElo")}
                {sortableHeader("wins", "Wins")}
                {sortableHeader("losses", "Losses")}
                {hasTies && sortableHeader("ties", "Ties")}
                {sortableHeader("winPercentage", "Win %")}
                {sortableHeader("pointsForPerGame", "Points Per Game")}
                {sortableHeader("pointsAgainstPerGame", "Points Allowed Per Game")}
                {sortableHeader("pointsDifferential", "Point Differential")}
              </tr>
            </thead>
            <tbody>
              {sortedTeams.map(team => (
                <tr key={team.id}>
                  <td className="team-name clickable" onClick={() => navigate(`/${league}/team/${team.abbreviation}`)}>
                    <img src={logoUrl(league, team.abbreviation)} alt={`${team.name} logo`} />
                    {team.name}
                  </td>
                  <td className="catelo">{formatCatelo(team.catelo)}</td>
                  <td>{team.wins}</td>
                  <td>{team.losses}</td>
                  {hasTies && <td>{team.ties}</td>}
                  <td>{team.winPercentage.toFixed(1)}</td>
                  <td>{team.pointsForPerGame.toFixed(1)}</td>
                  <td>{team.pointsAgainstPerGame.toFixed(1)}</td>
                  <td>{team.pointsDifferential.toFixed(1)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

export default StandingsPage;
