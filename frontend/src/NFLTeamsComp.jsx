import { useState, useEffect } from 'react';
import './index.css';

function NflTeamsComp() {
  const [nflTeams, setNflTeams] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/nflteams')  
      .then(response => response.json())
      .then(data => {
        setNflTeams(data.nfl_teams); 
        console.log("Fetched NFL teams:", data.nfl_teams);
      })
      .catch(error => console.error('Houston: we have a problem:', error));
  }, []);

  return (
    <>
      <nav />
      <h1>NFL Teams</h1>
      <div className = "default ">
        <div className = "table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Team</th>
                <th className="sortable">Wins</th>
                <th className="sortable">Losses</th>
                <th className="sortable">Ties</th>
                <th className="sortable">Win %</th>
                <th className="sortable">Points For</th>
                <th className="sortable">Points Against</th>
                <th className="sortable">Point Differential</th>
              </tr>
            </thead>
            <tbody>
              {nflTeams.map(team => (
                <tr key={team.id}>
                  <td>{team.name}</td>
                  <td>{team.wins}</td>
                  <td>{team.losses}</td>
                  <td>{team.ties}</td>
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

export default NflTeamsComp;