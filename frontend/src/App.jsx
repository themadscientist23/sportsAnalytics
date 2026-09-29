import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Nav from './Nav.jsx';
import Homepage from './Homepage.jsx';
import TeamsComp from './TeamsComp.jsx';
import TeamPage from './TeamPage.jsx';
import './index.css';

function NotFound() {
  return <h1>Error 404 - Airball</h1>;
}

function App() {

  return (
    <Router>
      <Nav />
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/nba" element={<TeamsComp league="nba" />} />
        <Route path="/nfl" element={<TeamsComp league="nfl" />} />
        <Route path="/mlb" element={<TeamsComp league="mlb" />} />
        <Route path="/nba/team/:abbreviation" element={<TeamPage league="nba" />} />
        <Route path="/nfl/team/:abbreviation" element={<TeamPage league="nfl" />} />
        <Route path="/mlb/team/:abbreviation" element={<TeamPage league="mlb" />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;