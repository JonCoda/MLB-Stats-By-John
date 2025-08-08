import streamlit as st
import requests

BASE_URL = "https://sportsdata.io/developers/api-documentation/mlb#standings"

def _make_request(url, error_message):
    """Helper function to make API requests and handle errors."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"{error_message}: {e}")
        return None

# --- API Functions ---

@st.cache_data(ttl=3600)
def get_team_standings(season="2024", league_ids="103,104"):
    url = f"{BASE_URL}/standings?leagueId={league_ids}&season={season}"
    return _make_request(url, f"Failed to fetch team standings for season {season}")

@st.cache_data(ttl=3600)
def get_player_stats(player_id, season="2024"):
    url = f"{BASE_URL}/people/{player_id}/stats?stats=season&season={season}"
    return _make_request(url, f"Failed to fetch stats for player ID {player_id}")

@st.cache_data(ttl=86400)
def find_player(player_name):
    url = f"{BASE_URL}/people/search?names={player_name}"
    data = _make_request(url, f"Error searching for player '{player_name}'")
    return data.get('people', []) if data else None

@st.cache_data(ttl=86400)
def get_player_info(player_id):
    """Get basic info for a single player by ID."""
    url = f"{BASE_URL}/people/{player_id}"
    data = _make_request(url, f"Error fetching info for player ID '{player_id}'")
    return data['people'][0] if data and data.get('people') else None

# --- Display Section (Streamlit Version) ---

def display_team_standings(season="2024"):
    """Fetches and displays team standings in a Streamlit-friendly format."""
    data = get_team_standings(season=season)
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
                    st.table(team_data)
                else:
                    st.write("No team records found for this division.")

            except KeyError:
                st.error("Could not parse division standings due to unexpected data format.")
    else:
        st.warning("Could not retrieve team standings at the moment.")

def display_player_stats(player_id, season="2024"):
    """Fetches and displays player stats using Streamlit metrics."""
    player_info = get_player_info(player_id)
    if not player_info:
        st.error(f"Could not retrieve information for player ID {player_id}.")
        return

    player_name = player_info.get('fullName', 'Unknown Player')
    st.subheader(f"Season Stats for {player_name}")
    data = get_player_stats(player_id, season=season)

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

def handle_player_search(player_input):
    """
    Handles the logic for searching a player by name or ID and updates session state.
    Provides immediate feedback if an ID is invalid.
    """
    # Reset previous results
    st.session_state.search_results = None
    st.session_state.selected_player_id = None

    if player_input.isdigit():
        # Validate player ID immediately
        if get_player_info(player_input):
            st.session_state.selected_player_id = player_input
        else:
            st.error(f"No player found with ID {player_input}.")
    else:
        # Handle name search
        results = find_player(player_input)
        if not results:
            st.warning(f"No players found matching '{player_input}'.")
        elif len(results) == 1:
            st.session_state.selected_player_id = results[0].get('id')
        else:
            st.session_state.search_results = results

if __name__ == "__main__":
    main()
