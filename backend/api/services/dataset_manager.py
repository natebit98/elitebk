import os
import requests
from .vector_store import update_dataset as update_vector_dataset
from basketball_reference_scraper.teams import get_schedule
import pandas

# list of NBA teams used to fetch schedules/games from basketball reference scraper
NBA_TEAMS = [
    "ATL","BOS","BRK","CHO","CHI","CLE","DAL","DEN","DET","GSW",
    "HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOP","NYK",
    "OKC","ORL","PHI","PHO","POR","SAC","SAS","TOR","UTA","WAS"
]

def fetch_latest_data(season):
    """
    Fetches schedule/results for all NBA teams for a given season.
    Returns a single combined DataFrame with duplicates removed.
    """
    all_games = []

    for team in NBA_TEAMS:
        try:
            df = get_schedule(team, season)
            df["TEAM"] = team  # tag source team
            all_games.append(df)
            print(f"Fetched {team} {season}")
        except Exception as e:
            print(f"Error fetching {team}: {e}")

    if not all_games:
        return None

    combined = pandas.concat(all_games, ignore_index=True)

    # Remove duplicates - this step necessary because each game 
    # appears twice (once from each involved team's schedule)
    combined = combined.drop_duplicates(subset=["DATE", "OPPONENT", "PTS", "OPP_PTS"])

    return combined

def preprocess_data(data):
    preprocessed_data = []

    for _, row in data.iterrows():
        date = row["DATE"]
        team = row["TEAM"]
        opponent = row["OPPONENT"]
        home_away = row["HOME/AWAY"]
        team_score = row["PTS"]
        opp_score = row["OPP_PTS"]

        # Determine home/away teams
        if home_away == "HOME":
            home_team = team
            away_team = opponent
        else:
            home_team = opponent
            away_team = team

        content = (
            f"{home_team} vs {away_team} - {date}\n"
            f"Location: {'Home' if home_away == 'HOME' else 'Away'}\n"
            f"Score: {team_score} - {opp_score}"
        )

        document = {
            "content": content,
            "metadata": {
                "source": "BasketballReference",
                "date": str(date),
                "home_team": home_team,
                "away_team": away_team,
                "team_score": team_score,
                "opponent_score": opp_score,
            }
        }

        preprocessed_data.append(document)

    return preprocessed_data

def update_dataset(season):
    latest_data = fetch_latest_data(season)

    if latest_data is not None:
        preprocessed_data = preprocess_data(latest_data)
        update_vector_dataset(preprocessed_data)
        print(f'Dataset updated successfully for all NBA teams from season {season}.')
    else:
        print(f'Failed to update dataset for all NBA teams from season {season}.')

if __name__ == '__main__':
    # Example usage: Update dataset for 2024 season
    update_dataset(2024)