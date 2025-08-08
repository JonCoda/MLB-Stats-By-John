# API Section
import requests


class MLBApi:
    BASE_URL = "https://api.com/mlb"
    
    def __init__(self, api_key=None):
        self.api_key = 'ba48316d0bc6c7d57e7415942bcb70b0' # Use the provided API key
    
    def get_headers(self):
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'  # Adjust header name if needed
        return headers
    
    def get_team_standings(self, season="2024"):
        url = f"{self.BASE_URL}/teams/standings?season={season}"
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch team standings from api.com")
            return None
    
    def get_player_stats(self, player_id, season="2024"):
        url = f"{self.BASE_URL}/players/{player_id}/stats?season={season}"
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            print(f"No stats found for player ID {player_id} (season {season}).")
            return None
    
# Display Section
def display_team_standings(api, season="2024"):
    data = api.get_team_standings(season)
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
