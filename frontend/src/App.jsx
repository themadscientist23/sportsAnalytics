import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Nav from './Nav.jsx';
import Homepage from './Homepage.jsx';
import NbaTeamsComp from './NBATeamsComp.jsx';
import NflTeamsComp from './NFLTeamsComp.jsx';
import MlbTeamsComp from './MLBTeamsComp.jsx';
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
        <Route path="/nba" element={<NbaTeamsComp />} />
        <Route path="/nfl" element={<NflTeamsComp />} />
        <Route path="/mlb" element={<MlbTeamsComp />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;