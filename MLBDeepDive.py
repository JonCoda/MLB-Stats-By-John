import requests
# Using thefuzz for "fuzzy" string matching to find the best result
# even with typos or partial names.
# You'll need to install it: pip install thefuzz python-Levenshtein
from thefuzz import process

API_BASE_URL = "https://statsapi.mlb.com/api/v1"

def find_team(team_name: str) -> dict | None:
    """
    Finds an MLB team by name using a fuzzy search.

    Args:
        team_name: The name of the team to search for.

    Returns:
        A dictionary containing the team's data if a good match is found, otherwise None.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/teams?sportId=1")
        response.raise_for_status()
        data = response.json()

        all_teams = data.get('teams', [])
        team_map = {team['name']: team for team in all_teams}

        best_match = process.extractOne(team_name, team_map.keys())

        if best_match and best_match[1] > 80:
            return team_map[best_match[0]]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching team information: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return None

def find_players(player_name: str) -> list | None:
    """
    Finds MLB players by name.

    Args:
        player_name: The name of the player to search for.

    Returns:
        A list of players found, or None if an error occurs.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/people/search?names={player_name}&active=true")
        response.raise_for_status()
        return response.json().get('people', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player information: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return None

def search_mlb_info():
    """Handles the user interface for searching teams and players."""
    search_type = input("Do you want to search for a 'team' or a 'player'? ").lower()
    if search_type == 'team':
        team_name = input("Enter the MLB team name: ")
        print(f"Searching for information about the MLB team: '{team_name}'...")
        found_team_data = find_team(team_name)
        if found_team_data:
            print("\n--- Team Information ---")
            print(f"Team Name: {found_team_data.get('name')}")
            print(f"Location: {found_team_data.get('locationName')}")
            print(f"Division: {found_team_data.get('division', {}).get('name')}")
            print(f"League: {found_team_data.get('league', {}).get('name')}")
            print(f"Venue: {found_team_data.get('venue', {}).get('name')}")
            print(f"Team ID: {found_team_data.get('id')}")
        else:
            print(f"Team '{team_name}' not found. Please check the name and try again.")

    elif search_type == 'player':
        player_name = input("Enter the MLB player name: ")
        print(f"Searching for information about the MLB player: {player_name}...")
        players_found = find_players(player_name)
        if players_found is None: # Indicates an error occurred
            return
        elif len(players_found) == 1:
            player = players_found[0]
            print("\n--- Player Information ---")
            print(f"Name: {player.get('fullName')}")
            print(f"Primary Position: {player.get('primaryPosition', {}).get('name', 'N/A')}")
            print(f"Current Team: {player.get('currentTeam', {}).get('name', 'N/A')}")
            print(f"Player ID: {player.get('id')}")
        elif len(players_found) > 1:
            print(f"\nFound multiple players for '{player_name}'. Please be more specific.")
            print("Possible matches:")
            for player in players_found:
                team_name = player.get('currentTeam', {}).get('name', 'N/A')
                print(f"- {player.get('fullName')} ({team_name})")
        else:
            print(f"Player '{player_name}' not found. Please check the spelling.")
    else:
        print("Invalid search type. Please enter 'team' or 'player'.")

if __name__ == "__main__":
    search_mlb_info()
