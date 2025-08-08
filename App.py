import requests

# Fetch MLB team standings
def get_team_standings():
    url = "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=2024"
    response = requests.get(url)
    data = response.json()
    print("MLB Team Standings (2024):\n")
    for record in data['records']:
        print(f"{record['league']['name']}:")
        for team in record['teamRecords']:
            name = team['team']['name']
            wins = team['wins']
            losses = team['losses']
            pct = team['winningPercentage']
            print(f"  {name}: {wins}-{losses} ({pct})")
        print()

# Fetch sample player stats (batting stats for 2024)
def get_player_stats(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season&season=2024"
    response = requests.get(url)
    data = response.json()
    if data['stats']:
        stats = data['stats'][0]['splits'][0]['stat']
        print(f"Player ID {player_id} Stats (2024):")
        print(f"  AVG: {stats.get('avg', 'N/A')}")
        print(f"  HR: {stats.get('homeRuns', 'N/A')}")
        print(f"  RBI: {stats.get('rbi', 'N/A')}")
        print(f"  OPS: {stats.get('ops', 'N/A')}")
        print()
    else:
        print(f"No stats found for player ID {player_id} (2024).\n")

if __name__ == "__main__":
    get_team_standings()
    # Example player IDs: 660271 (Aaron Judge), 605141 (Shohei Ohtani), 547989 (Mookie Betts)
    print("Sample Player Stats:\n")
    for pid in [660271, 605141, 547989]:
        get_player_stats(pid)
