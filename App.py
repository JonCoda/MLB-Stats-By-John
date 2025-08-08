# API Section
import requests


class MLBApi:
    # This is the base URL for the api-sports.io baseball API.
    BASE_URL = "https://v1.baseball.api-sports.io"

    def __init__(self, api_key):
        # The api-sports.io API requires an API key.
        if not api_key or api_key == "YOUR_API_SPORTS_KEY_HERE":
            raise ValueError("API key is required for api-sports.io. Please add it to the main script section.")
        self.api_key = 'ba48316d0bc6c7d57e7415942bcb70b0'


    def get_headers(self):
        # api-sports.io uses a custom header for authentication.
        # Refer to your API provider's documentation.
        return {
            'x-apisports-key': self.api_key
        }

    def get_team_standings(self, season="2024", league_ids="103,104"):
        # NOTE: The endpoint '/standings' and the parameters are from the old API.
        # You MUST update this URL path to match the api-sports.io documentation.
        url = f"{self.BASE_URL}/standings?leagueId={league_ids}&season={season}"
        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch team standings: {e}")
            return None

    def get_player_stats(self, player_id, season="2024"):
        # NOTE: The endpoint '/people/{player_id}/stats' is from the old API.
        # You MUST update this URL path to match the api-sports.io documentation.
        url = f"{self.BASE_URL}/people/{player_id}/stats?stats=season&season={season}"
        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch stats for player ID {player_id} (season {season}): {e}")
            return None

# Display Section
def display_team_standings(api, season="2024"):
    # WARNING: This function is written for the statsapi.mlb.com data structure.
    # It WILL FAIL with the api-sports.io API and must be rewritten
    # to match the new JSON response format.
    data = api.get_team_standings(season)
    if data and 'records' in data:
        print(f"MLB Team Standings ({season}):\n")
        for record in data['records']:
            print(f"{record['league']['name']}:")
            for team in record['teamRecords']:
                name = team['team']['name']
                wins = team['wins']
                losses = team['losses']
                pct = team['winningPercentage']
                print(f"  {name}: {wins}-{losses} ({pct})")
            print()
    else:
        print("Could not retrieve team standings.")

def display_player_stats(api, player_id, season="2024"):
    # WARNING: This function is written for the statsapi.mlb.com data structure.
    # It WILL FAIL with the api-sports.io API and must be rewritten
    # to match the new JSON response format.
    data = api.get_player_stats(player_id, season)
    if data and data.get('stats'):
        try:
            stats = data['stats'][0]['splits'][0]['stat']
            print(f"Player ID {player_id} Stats ({season}):")
            print(f"  AVG: {stats.get('avg', 'N/A')}")
            print(f"  HR: {stats.get('homeRuns', 'N/A')}")
            print(f"  RBI: {stats.get('rbi', 'N/A')}")
            print(f"  OPS: {stats.get('ops', 'N/A')}")
            print()
        except (IndexError, KeyError) as e:
            print(f"Could not parse stats for player ID {player_id}. Unexpected data format: {e}")
    else:
        print(f"No stats found for player ID {player_id} (season {season}).\n")


if __name__ == "__main__":
    # You must get an API key from api-sports.io and place it here.
    api_key = "YOUR_API_SPORTS_KEY_HERE"
    
    try:
        api = MLBApi(api_key=api_key)
        
        display_team_standings(api)

        while True:
            print("\nEnter a player ID to get their 2024 stats.")
            player_id_input = input("Or type 'exit' to quit: ")

            if player_id_input.lower() in ['exit', 'q']:
                print("\nExiting application. Goodbye!")
                break

            if player_id_input.isdigit():
                display_player_stats(api, player_id_input)
            else:
                print("\nInvalid input. Please enter a numeric player ID.")
    except ValueError as e:
        print(f"ERROR: {e}")        for record in data['records']:
            print(f"{record['league']['name']}:")
            for team in record['teamRecords']:
                name = team['team']['name']
                wins = team['wins']
                losses = team['losses']
                pct = team['winningPercentage']
                print(f"  {name}: {wins}-{losses} ({pct})")
            print()
    else:
        print("Could not retrieve team standings.")

def display_player_stats(api, player_id, season="2024"):
    data = api.get_player_stats(player_id, season)
    if data and data.get('stats'):
        try:
            stats = data['stats'][0]['splits'][0]['stat']
            print(f"Player ID {player_id} Stats ({season}):")
            print(f"  AVG: {stats.get('avg', 'N/A')}")
            print(f"  HR: {stats.get('homeRuns', 'N/A')}")
            print(f"  RBI: {stats.get('rbi', 'N/A')}")
            print(f"  OPS: {stats.get('ops', 'N/A')}")
            print()
        except (IndexError, KeyError) as e:
            print(f"Could not parse stats for player ID {player_id}. Unexpected data format: {e}")
    else:
        print(f"No stats found for player ID {player_id} (season {season}).\n")


if __name__ == "__main__":
    api = MLBApi()
    display_team_standings(api)

    while True:
        print("\nEnter a player ID to get their 2024 stats.")
        print("(Example IDs: 660271 for Aaron Judge, 605141 for Shohei Ohtani)")
        player_id_input = input("Or type 'exit' to quit: ")

        if player_id_input.lower() in ['exit', 'q']:
            print("\nExiting application. Goodbye!")
            break

        if player_id_input.isdigit():
            display_player_stats(api, player_id_input)
        else:
            print("\nInvalid input. Please enter a numeric player ID.")            print(f"{record['league']['name']}:")
            for team in record['teamRecords']:
                name = team['team']['name']
                wins = team['wins']
                losses = team['losses']
                pct = team['winningPercentage']
                print(f"  {name}: {wins}-{losses} ({pct})")
            print()
    else:
        print("Could not retrieve team standings.")

def display_player_stats(api, player_id, season="2024"):
    data = api.get_player_stats(player_id, season)
    if data and data.get('stats'):
        try:
            stats = data['stats'][0]['splits'][0]['stat']
            print(f"Player ID {player_id} Stats ({season}):")
            print(f"  AVG: {stats.get('avg', 'N/A')}")
            print(f"  HR: {stats.get('homeRuns', 'N/A')}")
            print(f"  RBI: {stats.get('rbi', 'N/A')}")
            print(f"  OPS: {stats.get('ops', 'N/A')}")
            print()
        except (IndexError, KeyError) as e:
            print(f"Could not parse stats for player ID {player_id}. Unexpected data format: {e}")
    else:
        print(f"No stats found for player ID {player_id} (season {season}).\n")


if __name__ == "__main__":
    api = MLBApi()
    display_team_standings(api)
    print("Sample Player Stats:\n")
    for pid in [660271, 605141, 547989]:
        display_player_stats(api, pid)    data = api.get_team_standings(season)
    if data:
        print(f"MLB Team Standings ({season}):\n")
        for team in data.get('teams', []):
            name = team.get('name', 'Unknown')
            wins = team.get('wins', 'N/A')
            losses = team.get('losses', 'N/A')
            pct = team.get('pct', 'N/A')
            print(f"  {name}: {wins}-{losses} ({pct})") # Corrected f-string
        print()

def display_player_stats(api, player_id, season="2024"):
    data = api.get_player_stats(player_id, season)
    if data:
        stats = data.get('stats', {})
        print(f"Player ID {player_id} Stats ({season}):")
        print(f"  AVG: {stats.get('avg', 'N/A')}")
        print(f"  HR: {stats.get('homeRuns', 'N/A')}")
        print(f"  RBI: {stats.get('rbi', 'N/A')}")
        print(f"  OPS: {stats.get('ops', 'N/A')}")
        print()
    
    
if __name__ == "__main__":
    # Input your API key here
    api_key = "YOUR_API_KEY_HERE"
    api = MLBApi(api_key=api_key)
    display_team_standings(api)
    print("Sample Player Stats:\n")
    for pid in [660271, 605141, 547989]:
        display_player_stats(api, pid)    # Example player IDs: 660271 (Aaron Judge), 605141 (Shohei Ohtani), 547989 (Mookie Betts)
    print("Sample Player Stats:\n")
    for pid in [660271, 605141, 547989]:
        get_player_stats(pid)
