import { Link } from 'react-router-dom';
import './Nav.css';

function Nav() {
    return (
        <header>
            <nav className="main-nav">
                <Link to="/" className="logo">
                    <img src="/simplelogo.png" alt="Sports Analytics Platform home" />
                </Link>
                <div className="nav-links">
                    <Link to="/nba">NBA</Link>
                    <Link to="/nfl">NFL</Link>
                    <Link to="/mlb">MLB</Link>
                </div>
            </nav>
        </header>
    );
}

export default Nav;
