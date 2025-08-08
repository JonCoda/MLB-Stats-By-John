# API Section
import requests


class MLBApi:
    # This is the base URL for the free public MLB Stats API.
    BASE_URL = "https://statsapi.mlb.com/api/v1"

    def __init__(self):
        # This API does not require an API key.
        pass

    def get_team_standings(self, season="2024", league_ids="103,104"):
        # Corrected endpoint for MLB Stats API
        url = f"{self.BASE_URL}/standings?leagueId={league_ids}&season={season}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch team standings for season {season}: {e}")
            return None

    def get_player_stats(self, player_id, season="2024"):
        # Corrected endpoint for MLB Stats API
        url = f"{self.BASE_URL}/people/{player_id}/stats?stats=season&season={season}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch stats for player ID {player_id} (season {season}): {e}")
            return None

    def find_player(self, player_name):
        """Search for a player by name."""
        url = f"{self.BASE_URL}/people/search?names={player_name}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('people', [])  # Return list of players, or empty list
        except requests.exceptions.RequestException as e:
            print(f"Error searching for player '{player_name}': {e}")
            return None

# Display Section
def display_team_standings(api, season="2024"):
    data = api.get_team_standings(season=season)
    if data is None:
        return  # Error message was already printed by the API method

    if 'records' in data and data['records']:
        print(f"MLB Team Standings ({season}):\n")
        for record in data['records']:
            try:
                # Display division name (e.g., "American League East")
                division_name = record['division']['name']
                print(f"{division_name}:")
                for team in record.get('teamRecords', []):
                    # Use .get() for safer access to nested data
                    name = team.get('team', {}).get('name', 'Unknown Team')
                    wins = team.get('wins', '?')
                    losses = team.get('losses', '?')
                    pct = team.get('winningPercentage', '.---')
                    print(f"  {name}: {wins}-{losses} ({pct})")
                print()
            except KeyError:
                print("  Error: Could not parse division standings due to unexpected data format.\n")
    else:
        print("Could not retrieve team standings or no records were found.")

def display_player_stats(api, player_id, season="2024"):
    data = api.get_player_stats(player_id, season=season)
    if data is None:
        return  # Error message was already printed by the API method

    if data.get('stats'):
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

# Application Logic Section
def select_player_from_search(api, player_name):
    """Handles the player search and selection logic, returning a player ID."""
    players_found = api.find_player(player_name)

    if players_found is None:
        return None  # API method already printed an error.

    if not players_found:
        print(f"\nNo players found matching '{player_name}'. Please try again.")
        return None

    if len(players_found) == 1:
        player = players_found[0]
        player_id = player.get('id')
        print(f"\nFound: {player.get('fullName', 'N/A')} (ID: {player_id})")
        return player_id
    else:
        # Handle multiple players
        print(f"\nMultiple players found for '{player_name}'. Please choose one:")
        for i, player in enumerate(players_found):
            team = player.get('currentTeam', {}).get('name', 'N/A')
            pos = player.get('primaryPosition', {}).get('abbreviation', 'N/A')
            print(f"  {i + 1}: {player.get('fullName', 'N/A')} ({pos}, {team})")
        try:
            choice = int(input("Enter the number of the player you want: "))
            if 1 <= choice <= len(players_found):
                return players_found[choice - 1].get('id')
            else:
                print("Invalid choice.")
                return None
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None

def run_interactive_session(api):
    """Runs the main interactive loop for the application."""
    while True:
        print("\nEnter a player name or ID to get their 2024 stats.")
        print("(e.g., 'Aaron Judge', 'Ohtani', or '660271')")
        player_input = input("Or type 'exit' to quit: ")

        if player_input.lower() in ['exit', 'q']:
            print("\nExiting application. Goodbye!")
            break

        player_id_to_fetch = None
        if player_input.isdigit():
            player_id_to_fetch = player_input
        else:
            player_id_to_fetch = select_player_from_search(api, player_input)

        if player_id_to_fetch:
            display_player_stats(api, player_id_to_fetch)

def main():
    """Main function to run the MLB Stats application."""
    api = MLBApi()
    display_team_standings(api)
    run_interactive_session(api)

if __name__ == "__main__":
    main()
def display_team_standings(api, season="2024"):
    data = api.get_team_standings(season)
    if data and 'records' in data:
        st.header(f"MLB Team Standings ({season})")
        for record in data['records']:
            league_name = record.get('league', {}).get('name', 'Unknown')
            st.subheader(league_name)
            for team in record.get('teamRecords', []):
                name = team.get('team', {}).get('name', 'Unknown')
                wins = team.get('wins', 'N/A')
                losses = team.get('losses', 'N/A')
                pct = team.get('winningPercentage', 'N/A')
                st.write(f"{name}: {wins}-{losses} ({pct})")
    else:
        st.warning("Could not retrieve team standings.")

def display_player_stats(api, player_id, season="2024"):
    data = api.get_player_stats(player_id, season)
    if data and data.get('stats'):
        splits = data['stats'][0].get('splits', [])
        if splits:
            stats = splits[0].get('stat', {})
            st.markdown(f"**Player ID {player_id} Stats ({season}):**")
            st.write(f"AVG: {stats.get('avg', 'N/A')}")
            st.write(f"HR: {stats.get('homeRuns', 'N/A')}")
            st.write(f"RBI: {stats.get('rbi', 'N/A')}")
            st.write(f"OPS: {stats.get('ops', 'N/A')}")
        else:
            st.warning(f"No stats found for player ID {player_id}.")
    else:
        st.warning(f"No stats found for player ID {player_id}.")

def main():
    st.title("MLB Stats Explorer")
    api = MLBApi()

    st.sidebar.header("Options")
    season = st.sidebar.text_input("Season", "2024")

    if st.sidebar.button("Fetch Team Standings"):
        display_team_standings(api, season)

    st.header("Player Stats Lookup")
    player_input = st.text_input("Enter player name or ID", "")
    if st.button("Search Player"):
        if player_input.isdigit():
            display_player_stats(api, player_input, season)
        elif player_input:
            players = api.find_player(player_input)
            if not players:
                st.warning("No players found.")
            elif len(players) == 1:
                pid = players[0].get('id')
                st.info(f"Found: {players[0].get('fullName', 'N/A')} (ID: {pid})")
                display_player_stats(api, pid, season)
            else:
                options = {f"{p.get('fullName', 'N/A')} ({p.get('primaryPosition', {}).get('abbreviation', '')}, {p.get('currentTeam', {}).get('name', '')})": p.get('id') for p in players}
                selected = st.selectbox("Choose player", list(options.keys()))
                if selected:
                    display_player_stats(api, options[selected], season)

if __name__ == "__main__":
    main()
