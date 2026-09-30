import argparse

from app.db.session import close_session, get_db_session
from app.sports.config import SPORTS

INITIAL_CATELO = 1000.0


def _seasons_with_unrated_games(session, game_model, rating_model):
    rows = (
        session.query(game_model.season)
        .outerjoin(rating_model, rating_model.game_id == game_model.id)
        .filter(game_model.postseason.is_(False))
        .filter(rating_model.game_id.is_(None))
        .distinct()
        .all()
    )
    return sorted(season for (season,) in rows)


def _process_season(session, config, season):
    team_model = config["team_model"]
    game_model = config["game_model"]
    rating_model = config["rating_model"]

    season_game_ids = session.query(game_model.id).filter(game_model.season == season)
    session.query(rating_model).filter(rating_model.game_id.in_(season_game_ids)).delete(synchronize_session=False)

    teams = {team.id: team for team in session.query(team_model).all()}
    games = (
        session.query(game_model)
        .filter(game_model.season == season)
        .filter(game_model.postseason.is_(False))
        .order_by(game_model.date, game_model.id)
        .all()
    )

    ratings = {}
    for game in games:
        home_pre = ratings.get(game.home_team_id, INITIAL_CATELO)
        away_pre = ratings.get(game.away_team_id, INITIAL_CATELO)
        result = config["process_game"](game, teams[game.home_team_id], teams[game.away_team_id], home_pre, away_pre)

        session.add(rating_model(game_id=game.id, home_pre_catelo=home_pre, away_pre_catelo=away_pre, **result))
        ratings[game.home_team_id] = result["home_post_catelo"]
        ratings[game.away_team_id] = result["away_post_catelo"]

    return len(games)


def process_games(sport):
    config = SPORTS[sport]
    session = get_db_session()
    try:
        for season in _seasons_with_unrated_games(session, config["game_model"], config["rating_model"]):
            count = _process_season(session, config, season)
            print(f"[{sport}:{season}] Rated {count} games.")
        session.commit()
    finally:
        close_session(session)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rate every regular-season game in seasons that have unrated games.")
    parser.add_argument("sport", choices=SPORTS.keys())
    args = parser.parse_args()

    process_games(args.sport)
