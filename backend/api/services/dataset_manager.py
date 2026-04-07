import os
import requests
from .vector_store import update_dataset as update_vector_dataset
import requests

def fetch_latest_data(league, season):
    base_url = 'https://www.thesportsdb.com/api/v1/json/123'
    endpoint = f'/eventsseason.php?id={league}&s={season}'
    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['events']
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data from TheSportsDB API: {e}')
        return None

def preprocess_data(data):
    preprocessed_data = []

    for event in data:
        # Extract relevant fields from the event data
        event_id = event['idEvent']
        event_date = event['dateEvent']
        event_time = event['strTime']
        home_team = event['strHomeTeam']
        away_team = event['strAwayTeam']
        home_score = event['intHomeScore']
        away_score = event['intAwayScore']

        # Create a preprocessed document
        document = {
            'content': f"{home_team} vs {away_team} - {event_date} {event_time}\nScore: {home_score} - {away_score}",
            'metadata': {
                'source': 'TheSportsDB',
                'event_id': event_id,
                'date': event_date,
                'home_team': home_team,
                'away_team': away_team
            }
        }

        preprocessed_data.append(document)

    return preprocessed_data

def update_dataset(league, season):
    latest_data = fetch_latest_data(league, season)

    if latest_data:
        preprocessed_data = preprocess_data(latest_data)
        update_vector_dataset(preprocessed_data)
        print(f'Dataset updated successfully for league {league} and season {season}.')
    else:
        print(f'Failed to update dataset for league {league} and season {season}.')

if __name__ == '__main__':
    # Example usage: Update dataset for English Premier League 2022-2023 season
    league_id = '4328'  # English Premier League ID
    season = '2022-2023'

    update_dataset(league_id, season)