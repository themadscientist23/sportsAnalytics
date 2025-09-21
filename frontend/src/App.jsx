import { useState , useEffect} from 'react'
import './App.css'

function App() {
  const [teams, setTeams] = useState([])

  useEffect(() => {
    fetch('http://127.0.0.1:8000/teams')
      .then(response => response.json())
      .then(data => {
        setTeams(data.teams);
        console.log("Fetched teams:", data.teams);
      })
      .catch(error => console.error('Houston: we have a problem:', error));
  }, []);


  return (
    <div className="something">
      <h1> NBA </h1>
      <ul>
        {teams.map(team => (
          <li key={team[0]}>
            {team[1]} — Wins: {team[2]}, Losses: {team[3]}
          </li>
        ))}
      </ul>
    </div>

  );

}

export default App;
