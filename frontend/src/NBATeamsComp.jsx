import { useState, useEffect } from 'react';
import './index.css';

function NBATeamsComp() {
  const [nba_teams, setNbaTeams] = useState([]);
  const [sort_config, setSortConfig] = useState({ key: 'null', direction: 'descending' });

  useEffect(() => {
    fetch('http://127.0.0.1:8000/nbateams')
      .then(response => response.json())
      .then(data => {
        const modified = data.map(team => {
          const games = team.wins + team.losses;
          const win_percentage = (games > 0 ? (team.wins / games) * 100 : 0).toFixed(1);
          const points_differential = (team.points_for - team.points_against) / games;
          return {
            ...team,
            win_percentage,
            points_differential,
          };
        });
        sortBy('catelo', modified);
        console.log("Fetched and modified NBA teams:", modified);
      })
      .catch(error => console.error('Houston: we have a problem:', error));
  }, []);

  const sortBy = (key, teams = nba_teams) => {
    let direction;

    if (sort_config.key === key && sort_config.direction === 'ascending') {
      direction = 'descending';
    } else if (sort_config.key === key && sort_config.direction === 'descending') {
      direction = 'ascending';
    } else {
      direction = 'descending';
    }

    setSortConfig({ key, direction });
    const sortedTeams = [...teams].sort((a, b) => {
      if (direction === 'ascending') {
        return a[key] > b[key] ? 1 : -1;
      } else {
        return a[key] < b[key] ? 1 : -1;
      }
    });
    setNbaTeams(sortedTeams);
  }


  return (
    <>
      <nav />
      <h1>NBA Teams</h1>
      <div className = "default ">
        <div className = "table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Team</th>
                <th onClick={() => sortBy("catelo")} className={`sortable ${sort_config.key === "catelo" ? (sort_config.direction === "ascending" ? "sort-asc" : "sort-desc") : ""}`}>
                        CatElo
                </th>
                <th onClick={() => sortBy("wins")} className={`sortable ${sort_config.key === "wins" ? (sort_config.direction === "ascending" ? "sort-asc" : "sort-desc") : ""}`}>
                        Wins 
                </th>
                <th onClick={() => sortBy("losses")} className={`sortable ${sort_config.key === "losses" ? (sort_config.direction === "ascending" ? "sort-asc" : "sort-desc") : ""}`}>
                        Losses 
                </th>
                <th onClick={() => sortBy("win_percentage")} className={`sortable ${sort_config.key === "win_percentage" ? (sort_config.direction === "ascending" ? "sort-asc" : "sort-desc") : ""}`}>
                        Win %
                </th>
                <th onClick={() => sortBy("points_for")} className={`sortable ${sort_config.key === "points_for" ? (sort_config.direction === "ascending" ? "sort-asc" : "sort-desc") : ""}`}>
                        Points For
                </th>
                <th onClick={() => sortBy("points_against")} className={`sortable ${sort_config.key === "points_against" ? (sort_config.direction === "ascending" ? "sort-asc" : "sort-desc") : ""}`}>
                        Points Against
                </th>
                <th onClick={() => sortBy("points_differential")} className={`sortable ${sort_config.key === "points_differential" ? (sort_config.direction === "ascending" ? "sort-asc" : "sort-desc") : ""}`}>
                        Point Differential
                </th>
              </tr>
            </thead>
            <tbody>
              {nba_teams.map(team => {
                const games = team.wins + team.losses;
                const pointsPerGame = (team.points_for / games).toFixed(1);
                const pointsAgainstPerGame = (team.points_against / games).toFixed(1);
                const pointDiffPerGame = team.points_differential.toFixed(1);

              return (
                <tr key={team.id}>
                  <td className="team_name">
                    <img src={`/logos/${team.name.replace(/ /g, '_')}.png`} alt={`${team.name} logo`} />
                    {team.name}
                  </td>
                  <td className="catelo">{team.catelo}</td>
                  <td>{team.wins}</td>
                  <td>{team.losses}</td>
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

export default NBATeamsComp;