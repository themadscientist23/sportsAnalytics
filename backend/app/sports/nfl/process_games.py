import math

K_FACTOR = 20
MAX_MOV_MULTIPLIER = 2.0


def process_game(game, home_team, away_team, home_rating, away_rating):
    expected_home_win = 1 / (1 + 10 ** (-(home_rating + home_team.home_adv - away_rating) / 400))

    if game.home_score > game.away_score:
        actual = 1.0
    elif game.away_score > game.home_score:
        actual = 0.0
    else:
        actual = 0.5

    margin = abs(game.home_score - game.away_score)
    mov_multiplier = min(math.log2(margin + 1), MAX_MOV_MULTIPLIER) if margin > 0 else 1.0
    change = K_FACTOR * mov_multiplier * (actual - expected_home_win)

    return {
        "home_post_catelo": home_rating + change,
        "away_post_catelo": away_rating - change,
    }
