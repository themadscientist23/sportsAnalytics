import { formatCatelo } from '../lib/format.js';
import './RecentGames.css';

function RecentGames({ history }) {
  return (
    <div className="game-history">
      <h2>Recent Games</h2>
      <div className="game-list">
        {history.slice(-10).reverse().map((game, index) => (
          <div key={index} className="game-item">
            <span className="game-date">
              {new Date(game.date).toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric',
              })}
            </span>
            <span className="game-opponent">
              {game.home ? 'vs' : '@'} {game.opponent}
            </span>
            <span className="game-score">{game.score}</span>
            <span className="game-catelo">{formatCatelo(game.catelo)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecentGames;
