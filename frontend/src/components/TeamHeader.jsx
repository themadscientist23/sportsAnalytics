import { logoUrl } from '../leagues.js';

function TeamHeader({ league, team }) {
  return (
    <div className="team-header">
      <img
        src={logoUrl(league, team.abbreviation)}
        alt={`${team.name} logo`}
        className="team-logo"
      />
      <div>
        <h1>{team.name}</h1>
        <div className="team-stats-summary">
          <div className="stat-item">
            <span className="stat-label">Current CatElo</span>
            <span className="stat-value">{Math.round(team.current_catelo)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TeamHeader;
