import './Nav.css';

function Nav() {
    return (
        <header>
            <nav className="main-nav">
                <a href="/" className="logo">
                    <img src="/simplelogo.png" alt="Logo" className="h-10 w-auto" />
                </a>
                <div className="nav-links">
                    <a href="/nba">NBA</a>
                    <a href="/nfl">NFL</a>
                    <a href="/mlb">MLB</a>
                </div>
            </nav>
        </header>
    );
}

export default Nav;
