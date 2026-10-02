import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Nav from './components/Nav.jsx';
import Homepage from './pages/Homepage.jsx';
import StandingsPage from './pages/StandingsPage.jsx';
import TeamPage from './pages/TeamPage.jsx';
import NotFound from './pages/NotFound.jsx';

function App() {
  return (
    <Router>
      <Nav />
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/nba" element={<StandingsPage league="nba" />} />
        <Route path="/nfl" element={<StandingsPage league="nfl" />} />
        <Route path="/mlb" element={<StandingsPage league="mlb" />} />
        <Route
          path="/nba/team/:abbreviation"
          element={<TeamPage league="nba" />}
        />
        <Route
          path="/nfl/team/:abbreviation"
          element={<TeamPage league="nfl" />}
        />
        <Route
          path="/mlb/team/:abbreviation"
          element={<TeamPage league="mlb" />}
        />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
