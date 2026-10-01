def _empty_row(team):
    return {
        "id": team.id,
        "name": team.name,
        "abbreviation": team.abbreviation,
        "wins": 0,
        "losses": 0,
        "ties": 0,
        "points_for": 0,
        "points_against": 0,
        "catelo": None,
    }


def standings(session, config, season):
    team_model = config["team_model"]
    game_model = config["game_model"]
    rating_model = config["rating_model"]

    teams = {team.id: team for team in session.query(team_model).all()}
    rows = (
        session.query(game_model, rating_model)
        .outerjoin(rating_model, rating_model.game_id == game_model.id)
        .filter(game_model.season == season)
        .order_by(game_model.date, game_model.id)
        .all()
    )

    table = {}
    for game, rating in rows:
        home = table.setdefault(game.home_team_id, _empty_row(teams[game.home_team_id]))
        away = table.setdefault(game.away_team_id, _empty_row(teams[game.away_team_id]))

        if rating is not None:
            home["catelo"] = rating.home_post_catelo
            away["catelo"] = rating.away_post_catelo

        if game.postseason:
            continue

        home["points_for"] += game.home_score
        home["points_against"] += game.away_score
        away["points_for"] += game.away_score
        away["points_against"] += game.home_score

        if game.home_score > game.away_score:
            home["wins"] += 1
            away["losses"] += 1
        elif game.away_score > game.home_score:
            away["wins"] += 1
            home["losses"] += 1
        else:
            home["ties"] += 1
            away["ties"] += 1

    return list(table.values())


def seasons(session, config):
    game_model = config["game_model"]
    return [season for (season,) in session.query(game_model.season).distinct().order_by(game_model.season)]


def catelo_history(session, config, team_id, season):
    team_model = config["team_model"]
    game_model = config["game_model"]
    rating_model = config["rating_model"]

    abbreviations = {team.id: team.abbreviation for team in session.query(team_model).all()}
    rows = (
        session.query(game_model, rating_model)
        .join(rating_model, rating_model.game_id == game_model.id)
        .filter(game_model.season == season)
        .filter((game_model.home_team_id == team_id) | (game_model.away_team_id == team_id))
        .order_by(game_model.date, game_model.id)
        .all()
    )

    history = []
    for game, rating in rows:
        is_home = game.home_team_id == team_id
        history.append(
            {
                "date": game.date.isoformat(),
                "catelo": rating.home_post_catelo if is_home else rating.away_post_catelo,
                "opponent": abbreviations[game.away_team_id if is_home else game.home_team_id],
                "home": is_home,
                "score": f"{game.home_score}-{game.away_score}" if is_home else f"{game.away_score}-{game.home_score}",
            }
        )
    return history
