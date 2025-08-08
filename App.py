import streamlit as st
import requests

class MLBApi:
    BASE_URL = "https://statsapi.mlb.com/api/v1"

    def __init__(self, api_key=None):
        self.api_key = api_key  # For APIs that require a key

    def get_team_standings(self, season="2024"):
        url = f"{self.BASE_URL}/standings?season={season}&leagueId=103,104"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch team standings for season {season}: {e}")
            return None

    def get_player_stats(self, player_id, season="2024"):
        url = f"{self.BASE_URL}/people/{player_id}/stats?stats=season&season={season}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch stats for player ID {player_id} (season {season}): {e}")
            return None

    def find_player(self, player_name):
        url = f"{self.BASE_URL}/people/search?names={player_name}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('people', [])
        except requests.exceptions.RequestException as e:
            st.error(f"Error searching for player '{player_name}': {e}")
            return None

def display_team_standings(api, season="2024"):
    data = api.get_team_standings(season=season)
    if data and 'records' in data:
        st.header(f"MLB Team Standings ({season})")
        for record in data['records']:
            league = record.get('league', {})
            league_name = league.get('name', str(league))
            st.subheader(f"{league_name}")
            standings = []
            for team in record.get('teamRecords', []):
                name = team.get('team', {}).get('name', 'Unknown')
                wins = team.get('wins', 'N/A')
                losses = team.get('losses', 'N/A')
                pct = team.get('winningPercentage', 'N/A')
                standings.append(f"{name}: {wins}-{losses} ({pct})")
            st.write("\n".join(standings))
    else:
        st.warning("Could not retrieve team standings.")

def display_player_stats(api, player_id, season="2024"):
    data = api.get_player_stats(player_id, season=season)
    if data and data.get('stats'):
        try:
            splits = data['stats'][0].get('splits', [])
            if not splits:
                st.warning(f"No stats found for player ID {player_id} (season {season}).")
                return
            stats = splits[0].get('stat', {})
            st.markdown(f"**Player ID {player_id} Stats ({season}):**")
            st.write(f"AVG: {stats.get('avg', 'N/A')}")
            st.write(f"HR: {stats.get('homeRuns', 'N/A')}")
            st.write(f"RBI: {stats.get('rbi', 'N/A')}")
            st.write(f"OPS: {stats.get('ops', 'N/A')}")
        except (IndexError, KeyError, TypeError) as e:
            st.error(f"Could not parse stats for player ID {player_id}. Unexpected data format: {e}")
    else:
        st.warning(f"No stats found for player ID {player_id} (season {season}).")

def main():
    st.title("MLB Stats Explorer")

    api = MLBApi()

    st.sidebar.header("Options")
    season = st.sidebar.text_input("Season", "2024")

    expander = st.expander("Show Team Standings")
    with expander:
        if st.button("Fetch Team Standings"):
            display_team_standings(api, season)

    st.header("Player Stats Lookup")
    player_input = st.text_input("Enter player name or ID", "")
    if st.button("Search Player"):
        if player_input.isdigit():
            display_player_stats(api, player_input, season)
        elif player_input:
            players_found = api.find_player(player_input)
            if not players_found:
                st.warning(f"No players found matching '{player_input}'. Please try again.")
            elif len(players_found) == 1:
                player = players_found[0]
                st.info(f"Found: {player.get('fullName', 'N/A')} (ID: {player.get('id', 'N/A')})")
                display_player_stats(api, player.get('id'), season)
            else:
                st.write(f"Multiple players found for '{player_input}'. Please choose one:")
                options = {f"{p.get('fullName', 'N/A')} ({p.get('primaryPosition', {}).get('abbreviation', 'N/A')}, {p.get('currentTeam', {}).get('name', 'N/A')})": p.get('id') for p in players_found}
                selected_name = st.selectbox("Players", list(options.keys()))
                if selected_name:
                    selected_id = options[selected_name]
                    display_player_stats(api, selected_id, season)

if __name__ == "__main__":
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            # Some APIs return 'people', others may return 'results'
            return data.get('people', [])
        except requests.exceptions.RequestException as e:
            print(f"Error searching for player '{player_name}': {e}")
            return None

def display_team_standings(api, season="2024"):
    data = api.get_team_standings(season=season)
    if data and 'records' in data:
        print(f"MLB Team Standings ({season}):\n")
        for record in data['records']:
            league = record.get('league', {})
            league_name = league.get('name', str(league))
            print(f"{league_name}:")
            for team in record.get('teamRecords', []):
                name = team.get('team', {}).get('name', 'Unknown')
                wins = team.get('wins', 'N/A')
                losses = team.get('losses', 'N/A')
                pct = team.get('winningPercentage', 'N/A')
                print(f"  {name}: {wins}-{losses} ({pct})")
            print()
    else:
        print("Could not retrieve team standings.")

def display_player_stats(api, player_id, season="2024"):
    data = api.get_player_stats(player_id, season=season)
    if data and data.get('stats'):
        try:
            splits = data['stats'][0].get('splits', [])
            if not splits:
                print(f"No stats found for player ID {player_id} (season {season}).\n")
                return
            stats = splits[0].get('stat', {})
            print(f"Player ID {player_id} Stats ({season}):")
            print(f"  AVG: {stats.get('avg', 'N/A')}")
            print(f"  HR: {stats.get('homeRuns', 'N/A')}")
            print(f"  RBI: {stats.get('rbi', 'N/A')}")
            print(f"  OPS: {stats.get('ops', 'N/A')}")
            print()
        except (IndexError, KeyError, TypeError) as e:
            print(f"Could not parse stats for player ID {player_id}. Unexpected data format: {e}")
    else:
        print(f"No stats found for player ID {player_id} (season {season}).\n")

if __name__ == "__main__":
    api = MLBApi()
    display_team_standings(api)

    while True:
        print("\nEnter a player name or ID to get their 2024 stats.")
        print("(e.g., 'Aaron Judge', 'Ohtani', or '660271')")
        player_input = input("Or type 'exit' to quit: ")

        if player_input.lower() in ['exit', 'q']:
            print("\nExiting application. Goodbye!")
            break

        if player_input.isdigit():
            display_player_stats(api, player_input)
            continue

        players_found = api.find_player(player_input)
        if not players_found:
            print(f"\nNo players found matching '{player_input}'. Please try again.")
            continue

        if len(players_found) == 1:
            player = players_found[0]
            print(f"\nFound: {player.get('fullName', 'N/A')} (ID: {player.get('id', 'N/A')})")
            display_player_stats(api, player.get('id'))
        else:
            print(f"\nMultiple players found for '{player_input}'. Please choose one:")
            for i, player in enumerate(players_found):
                team = player.get('currentTeam', {}).get('name', 'N/A')
                pos = player.get('primaryPosition', {}).get('abbreviation', 'N/A')
                print(f"  {i + 1}: {player.get('fullName', 'N/A')} ({pos}, {team})")
            try:
                choice = int(input("Enter the number of the player you want: "))
                if 1 <= choice <= len(players_found):
                    pid = players_found[choice - 1].get('id')
                    display_player_stats(api, pid)
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a number.")        except requests.exceptions.RequestException as e:
            print(f"Error searching for player '{player_name}': {e}")
            return None

def display_team_standings(api, season="2024"):
    data = api.get_team_standings(season=season)
    if data and 'records' in data:
        print(f"MLB Team Standings ({season}):\n")
        for record in data['records']:
            league_name = record['league']['name'] if isinstance(record['league'], dict) else record['league']
            print(f"{league_name}:")
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
    data = api.get_player_stats(player_id, season=season)
    if data and data.get('stats'):
        try:
            splits = data['stats'][0].get('splits', [])
            if not splits:
                print(f"No stats found for player ID {player_id} (season {season}).\n")
                return
            stats = splits[0].get('stat', {})
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
        print("\nEnter a player name or ID to get their 2024 stats.")
        print("(e.g., 'Aaron Judge', 'Ohtani', or '660271')")
        player_input = input("Or type 'exit' to quit: ")

        if player_input.lower() in ['exit', 'q']:
            print("\nExiting application. Goodbye!")
            break

        # If the input is a number, treat it as an ID directly
        if player_input.isdigit():
            display_player_stats(api, player_input)
            continue

        # If it's not a number, search by name
        players_found = api.find_player(player_input)

        if players_found is None or len(players_found) == 0:
            print(f"\nNo players found matching '{player_input}'. Please try again.")
            continue

        player_id_to_fetch = None
        if len(players_found) == 1:
            player = players_found[0]
            print(f"\nFound: {player.get('fullName', 'N/A')} (ID: {player.get('id', 'N/A')})")
            player_id_to_fetch = player.get('id')
        else:
            print(f"\nMultiple players found for '{player_input}'. Please choose one:")
            for i, player in enumerate(players_found):
                team = player.get('currentTeam', {}).get('name', 'N/A')
                pos = player.get('primaryPosition', {}).get('abbreviation', 'N/A')
                print(f"  {i + 1}: {player.get('fullName', 'N/A')} ({pos}, {team})")
            try:
                choice = int(input("Enter the number of the player you want: "))
                if 1 <= choice <= len(players_found):
                    player_id_to_fetch = players_found[choice - 1].get('id')
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if player_id_to_fetch:
            display_player_stats(api, player_id_to_fetch)       
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response()
        return data.get('people', [])  # Return list of players, or empty list
        except requests.exceptions.RequestException as e:
            print(f"Error searching for player '{player_name}': {e}")
            return None

# Display Section
def display_team_standings(api, season="2024"):
    data = api.get_team_standings(season=season)
    if data and 'records' in data:
        print(f"MLB Team Standings ({season}):\n")
        for record in data['records']:
            print(f"{record['league']}:")
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
    data = api.get_player_stats(player_id, season=season)
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
        print("\nEnter a player name or ID to get their 2024 stats.")
        print("(e.g., 'Aaron Judge', 'Ohtani', or '660271')")
        player_input = input("Or type 'exit' to quit: ")

        if player_input.lower() in ['exit', 'q']:
            print("\nExiting application. Goodbye!")
            break

        # If the input is a number, treat it as an ID directly
        if player_input.isdigit():
            display_player_stats(api, player_input)
            continue

        # If it's not a number, search by name
        players_found = api.find_player(player_input)

        if not players_found:
            print(f"\nNo players found matching '{player_input}'. Please try again.")
            continue

        player_id_to_fetch = None
        if len(players_found) == 1:
            player = players_found[0]
            print(f"\nFound: {player.get('fullName', 'N/A')} (ID: {player.get('id', 'N/A')})")
            player_id_to_fetch = player.get('id')
        else:
            print(f"\nMultiple players found for '{player_input}'. Please choose one:")
            for i, player in enumerate(players_found):
                team = player.get('currentTeam', {}).get('name', 'N/A')
                pos = player.get('primaryPosition', {}).get('abbreviation', 'N/A')
                print(f"  {i + 1}: {player.get('fullName', 'N/A')} ({pos}, {team})")
            try:
                choice = int(input("Enter the number of the player you want: "))
                if 1 <= choice <= len(players_found):
                    player_id_to_fetch = players_found[choice - 1].get('id')
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if player_id_to_fetch:
            display_player_stats(api, player_id_to_fetch)        # You MUST update this URL path to match the api-sports.io documentation.
        url = f"{self.BASE_URL}/people/{player_id}/stats?stats=season&season={season}"
        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch stats for player ID {player_id} (season {season}): {e}")

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
        print(f"ERROR: {e}")        
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
            print("\nInvalid input. Please enter a numeric player ID.")            
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
        display_player_stats(api, pid)    
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
