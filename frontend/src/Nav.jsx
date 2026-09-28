import { Link } from 'react-router-dom';
import './Nav.css';

function Nav() {
    return (
        <header>
            <nav className="main-nav">
                <Link to="/" className="logo">
                    <img src="/simplelogo.png" alt="Logo" className="h-10 w-auto" />
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
