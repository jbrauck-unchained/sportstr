from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

def check_sports_season(sports_seasons):
    today = datetime.today()
    in_season_sports = []

    for sport, season in sports_seasons.items():
        start_date, end_date = season
        if start_date <= today <= end_date:
            in_season_sports.append(sport)

    return in_season_sports

def seasons():
    sports_seasons = {
        "football/nfl": (datetime(2023, 9, 8), datetime(2024, 2, 4)),
        "basketball/mens-college-basketball": (datetime(2023, 10, 1), datetime(2024, 4, 8)),
        "basketball/nba": (datetime(2023, 10, 1), datetime(2024, 6, 25)),
        "baseball/mlb": (datetime(2023, 10, 1), datetime(2024, 4, 8)),
    }
    in_season_sports = check_sports_season(sports_seasons)
    logging.info(f"Sports in season: {in_season_sports}")
    return in_season_sports
