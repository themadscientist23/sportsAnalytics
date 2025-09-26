import { useState, useEffect } from 'react';
import './index.css';

function NBATeamsComp() {
  const [nba_teams, setNbaTeams] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/nbateams')  
      .then(response => response.json())
      .then(data => {
        setNbaTeams(data.nba_teams); 
        console.log("Fetched NBA teams:", data.nba_teams);
      })
      .catch(error => console.error('Houston: we have a problem:', error));
  }, []);

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
                <th className = "sortable">CatElo</th>
                <th className = "sortable">Name</th>
                <th className="sortable">Wins</th>
                <th className="sortable">Losses</th>
                <th className="sortable">Win %</th>
                <th className="sortable">Points For</th>
                <th className="sortable">Points Against</th>
                <th className="sortable">Point Differential</th>
              </tr>
            </thead>
            <tbody>
              {nba_teams.map(team => (
                <tr key={team.id}>
                  <td>{team.catelo}</td>
                  <td>{team.name}</td>
                  <td>{team.wins}</td>
                  <td>{team.losses}</td>
                  <td>{team.win_percentage}</td>
                  <td>{team.points_for}</td>
                  <td>{team.points_against}</td>
                  <td>{team.points_differential}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

export default NBATeamsComp;