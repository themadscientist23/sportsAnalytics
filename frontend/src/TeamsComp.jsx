import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_URL } from './api.js';
import './index.css';

// Each league's teams table is identical apart from these bits.
const LEAGUE_CONFIG = {
  nba: { title: 'NBA Teams', hasTies: false },
  nfl: { title: 'NFL Teams', hasTies: true },
  mlb: { title: 'MLB Teams', hasTies: false },
};

function TeamsComp({ league }) {
  const { title, hasTies } = LEAGUE_CONFIG[league];
  const navigate = useNavigate();
  const [teams, setTeams] = useState([]);
  const [sort_config, setSortConfig] = useState({ key: 'null', direction: 'descending' });

  const sortBy = (key, teams_to_sort = teams) => {
    let direction;

    if (sort_config.key === key && sort_config.direction === 'ascending') {
      direction = 'descending';
    } else if (sort_config.key === key && sort_config.direction === 'descending') {
      direction = 'ascending';
    } else {
      direction = 'descending';
    }

    setSortConfig({ key, direction });
    const sortedTeams = [...teams_to_sort].sort((a, b) => {
      if (direction === 'ascending') {
        return a[key] > b[key] ? 1 : -1;
      } else {
        return a[key] < b[key] ? 1 : -1;
      }
    });
    setTeams(sortedTeams);
  }

  useEffect(() => {
    fetch(`${API_URL}/${league}/seasons`)
      .then(response => response.json())
      .then(seasons => fetch(`${API_URL}/${league}/seasons/${seasons[seasons.length - 1]}/teams`))
      .then(response => response.json())
      .then(data => {
        const modified = data.map(team => {
          const games = team.wins + team.losses + (hasTies ? team.ties : 0);
          const win_percentage = (games > 0 ? (team.wins / games) * 100 : 0).toFixed(1);
          const points_differential = games > 0 ? (team.points_for - team.points_against) / games : 0;
          return {
            ...team,
            win_percentage,
            points_differential,
          };
        });
        sortBy('catelo', modified);
        console.log(`Fetched and modified ${league.toUpperCase()} teams:`, modified);
      })
      .catch(error => console.error('Houston: we have a problem:', error));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [league]);

  const sortableHeader = (key, label) => (
    <th onClick={() => sortBy(key)} className={`sortable ${sort_config.key === key ? (sort_config.direction === "ascending" ? "sort-asc" : "sort-desc") : ""}`}>
      {label}
    </th>
  );

  return (
    <>
      <nav />
      <h1>{title}</h1>
      <div className = "default ">
        <div className = "table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Team</th>
                {sortableHeader("catelo", "CatElo")}
                {sortableHeader("wins", "Wins")}
                {sortableHeader("losses", "Losses")}
                {hasTies && sortableHeader("ties", "Ties")}
                {sortableHeader("win_percentage", "Win %")}
                {sortableHeader("points_for", "Points For")}
                {sortableHeader("points_against", "Points Against")}
                {sortableHeader("points_differential", "Point Differential")}
              </tr>
            </thead>
            <tbody>
              {teams.map(team => {
                const games = team.wins + team.losses + (hasTies ? team.ties : 0);
                const pointsPerGame = games > 0 ? (team.points_for / games).toFixed(1) : '0.0';
                const pointsAgainstPerGame = games > 0 ? (team.points_against / games).toFixed(1) : '0.0';
                const pointDiffPerGame = team.points_differential.toFixed(1);

              return (
                <tr key={team.id}>
                  <td className="team_name clickable" onClick={() => navigate(`/${league}/team/${team.abbreviation}`)}>
                    <img src={`/logos/${league}/${team.abbreviation}.png`} alt={`${team.name} logo`} />
                    {team.name}
                  </td>
                  <td className="catelo">{team.catelo}</td>
                  <td>{team.wins}</td>
                  <td>{team.losses}</td>
                  {hasTies && <td>{team.ties}</td>}
                  <td>{team.win_percentage}</td>
                  <td>{pointsPerGame}</td>
                  <td>{pointsAgainstPerGame}</td>
                  <td>{pointDiffPerGame}</td>
                </tr>
              );
            })}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

export default TeamsComp;
