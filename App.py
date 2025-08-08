import streamlit_app as st
import pandas as pd
import requests

# --- API Section ---

class MLBApi:
    BASE_URL = "https://statsapi.mlb.com/api/v1"

    def _make_request(self, url, error_message): # Caching is now handled by public methods
        """Helper function to make API requests and handle errors."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"{error_message}: {e}")
            return None

    # The _self parameter is used because Streamlit's caching mechanism hashes
    # the function's code, and using 'self' can sometimes lead to issues.
    # ttl sets the cache expiration time in seconds (e.g., 3600 = 1 hour).
    @st.cache_data(ttl=3600)
    def get_team_standings(_self, season="2024", league_ids="103,104"):
        url = f"{_self.BASE_URL}/standings?leagueId={league_ids}&season={season}"
        return _self._make_request(url, f"Failed to fetch team standings for season {season}")

    @st.cache_data(ttl=3600)
    def get_player_stats(_self, player_id, season="2024"):
        url = f"{_self.BASE_URL}/people/{player_id}/stats?stats=season&season={season}"
        return _self._make_request(url, f"Failed to fetch stats for player ID {player_id}")

    @st.cache_data(ttl=86400) # Player names and IDs don't change often
    def find_player(_self, player_name):
        url = f"{_self.BASE_URL}/people/search?names={player_name}"
        data = _self._make_request(url, f"Error searching for player '{player_name}'")
        return data.get('people', []) if data else None

    @st.cache_data(ttl=86400)
    def get_player_info(_self, player_id):
        """Get basic info for a single player by ID."""
        url = f"{_self.BASE_URL}/people/{player_id}"
        data = _self._make_request(url, f"Error fetching info for player ID '{player_id}'")
        return data['people'][0] if data and data.get('people') else None

# --- Display Section (Streamlit Version) ---

def display_team_standings(api, season="2024"):
    """Fetches and displays team standings in a Streamlit-friendly format."""
    data = api.get_team_standings(season=season)
    if data and 'records' in data:
        for record in data['records']:
            try:
                division_name = record['division']['name']
                st.subheader(division_name)

                team_data = []
                for team in record.get('teamRecords', []):
                    team_data.append({
                        "Team": team.get('team', {}).get('name', 'N/A'),
                        "W": team.get('wins', 0),
                        "L": team.get('losses', 0),
                        "Pct": team.get('winningPercentage', '.000'),
                        "GB": team.get('gamesBack', '-'),
                        "Streak": team.get('streak', {}).get('streakCode', '-')
                    })

                if team_data:
                    df = pd.DataFrame(team_data)
                    st.dataframe(df, hide_index=True, use_container_width=True)
                else:
                    st.write("No team records found for this division.")

            except KeyError:
                st.error("Could not parse division standings due to unexpected data format.")
    else:
        st.warning("Could not retrieve team standings at the moment.")

def display_player_stats(api, player_id, season="2024"):
    """Fetches and displays player stats using Streamlit metrics."""
    player_info = api.get_player_info(player_id)
    if not player_info:
        st.error(f"Could not retrieve information for player ID {player_id}.")
        return

    player_name = player_info.get('fullName', 'Unknown Player')
    st.subheader(f"Season Stats for {player_name}")

    data = api.get_player_stats(player_id, season=season)

    if data and data.get('stats') and data['stats'][0].get('splits'):
        try:
            stats = data['stats'][0]['splits'][0]['stat']
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Batting Avg", stats.get('avg', 'N/A'))
            col2.metric("Home Runs", stats.get('homeRuns', 'N/A'))
            col3.metric("RBIs", stats.get('rbi', 'N/A'))
            col4.metric("OPS", stats.get('ops', 'N/A'))
        except (IndexError, KeyError):
            st.warning(f"Could not parse stats for {player_name}. Format may be unexpected.")
    else:
        st.info(f"No {season} stats found for {player_name} (ID: {player_id}). They may be a pitcher or have not played this season.")

def handle_player_search(api, player_input):
    """
    Handles the logic for searching a player by name or ID and updates session state.
    Provides immediate feedback if an ID is invalid.
    """
    # Reset previous results
    st.session_state.search_results = None
    st.session_state.selected_player_id = None

    if player_input.isdigit():
        # Validate player ID immediately
        if api.get_player_info(player_input):
            st.session_state.selected_player_id = player_input
        else:
            st.error(f"No player found with ID {player_input}.")
    else:
        # Handle name search
        results = api.find_player(player_input)
        if not results:
            st.warning(f"No players found matching '{player_input}'.")
        elif len(results) == 1:
            st.session_state.selected_player_id = results[0].get('id')
        else:
            st.session_state.search_results = results

# --- Streamlit App Main Logic ---

def main():
    """Main function to run the MLB Stats Streamlit application."""
    st.set_page_config(page_title="MLB Stats Viewer", layout="wide")
    st.title("⚾ MLB Stats Viewer")

    api = MLBApi()

    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'selected_player_id' not in st.session_state:
        st.session_state.selected_player_id = None

    # --- Team Standings Section ---
    with st.expander("View 2024 Team Standings", expanded=True):
        display_team_standings(api)

    st.divider()

    # --- Player Search Section ---
    st.header("Player Stat Lookup")
    with st.form(key='player_search_form'):
        player_input = st.text_input("Enter a player name or ID (e.g., 'Aaron Judge', '660271')")
        submit_button = st.form_submit_button(label='Search')

    if submit_button and player_input:
        handle_player_search(api, player_input)

    # --- Display Logic for Search Results ---
    # This logic runs after the search is handled and the state is updated.
    if st.session_state.search_results:
        st.subheader("Multiple players found. Please choose one:")
        player_options = {
            f"{p.get('fullName', 'N/A')} ({p.get('primaryPosition', {}).get('abbreviation', 'N/A')}, {p.get('currentTeam', {}).get('name', 'N/A')})": p.get('id')
            for p in st.session_state.search_results
        }
        # When a user selects a player, we update the state and rerun the app
        # to immediately show the selected player's stats.
        selected_option = st.radio("Select a player:", options=player_options.keys(), index=None, key="player_choice")
        if selected_option:
            st.session_state.selected_player_id = player_options[selected_option]
            st.session_state.search_results = None
            st.rerun()
    elif st.session_state.selected_player_id:
        display_player_stats(api, st.session_state.selected_player_id)

if __name__ == "__main__":
    main()        url = f"{self.BASE_URL}/people/search?names={player_name}"
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
