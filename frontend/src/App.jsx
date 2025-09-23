import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [nbaTeams, setNbaTeams] = useState([]);

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
    <div>
      <h1>NBA Teams</h1>
      <table>
        <thead>
          <tr>
            <th>Team</th>
            <th>Wins</th>
            <th>Losses</th>
            <th>Win %</th>
            <th>Points For</th>
            <th>Points Against</th>
            <th>Point Differential</th>
          </tr>
        </thead>
        <tbody>
          {nbaTeams.map(team => (
            <tr key={team.id}>
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
  );
}

export default App;