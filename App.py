import streamlit as st
import requests
import datetime
import json # This import is necessary for pretty-printing JSON to the console for debugging

# Base URL for the SportsData.io MLB API.
# IMPORTANT: Verify this URL and specific endpoints with SportsData.io documentation.
MLB_API_BASE = "https://api.sportsdata.io/v3/mlb/scores/json"

# IMPORTANT: Replace "YOUR_API_KEY" with your actual SportsData.io subscription key.
# This is the most critical part for data retrieval!
API_KEY = "3031838cee374a47a9ccac67652ae731"

def make_api_request(endpoint, error_msg):
    """
    Makes a GET request to the SportsData.io MLB API, handling API key validation and errors.
    Includes print statements to help debug the raw API response.
    """
    if API_KEY == "YOUR_API_KEY":
        st.error("Please replace 'YOUR_API_KEY' with your actual SportsData.io API key to fetch data.")
        print("[DEBUG] API_KEY is still the placeholder. No API call will be made.")
        return {}

    try:
        url = f"{MLB_API_BASE}/{endpoint}?key={API_KEY}"
        st.info(f"Fetching data from: {url.split('?')[0]}...") # Show base URL without API key for privacy
        
        print(f"\n[DEBUG] Attempting API call to URL: {url}") # Print the full URL being requested

        response = requests.get(url)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)

        data = response.json() # This converts the JSON text into a Python dictionary/list
        print(f"[DEBUG] Raw JSON response for endpoint '{endpoint}':")
        print(json.dumps(data, indent=2)) # Pretty print the raw JSON for inspection
        return data
    except requests.exceptions.HTTPError as e:
        st.error(f"{error_msg} - HTTP Error {e.response.status_code}. Check API key and endpoint URL.")
        print(f"[ERROR] HTTP Error for '{endpoint}': {e.response.status_code} - Response Body: {e.response.text}")
        return {}
    except requests.exceptions.ConnectionError:
        st.error(f"{error_msg} - Connection Error. Check your internet connection.")
        print(f"[ERROR] Connection Error for '{endpoint}'.")
        return {}
    except requests.exceptions.Timeout:
        st.error(f"{error_msg} - Timeout Error. The request took too long.")
        print(f"[ERROR] Timeout Error for '{endpoint}'.")
        return {}
    except requests.exceptions.RequestException as e:
        st.error(f"{error_msg} - An unexpected error occurred: {e}")
        print(f"[ERROR] Unexpected Request Exception for '{endpoint}': {e}")
        return {}

def get_current_season_year():
    """
    Determines the current MLB season year from the API or falls back to the calendar year.
    """
    data = make_api_request("CurrentSeason", "Couldn't fetch current MLB season from API.")
    if data and isinstance(data, dict) and 'Season' in data:
        try:
            return int(data['Season'])
        except ValueError:
            st.warning("Could not parse current season year from API response.")
    st.info("Falling back to current calendar year as API did not provide current season.")
    return datetime.datetime.now().year

@st.cache_data(ttl=3600)
def get_team_standings_data(season):
    """Fetches raw team standings data for a given season."""
    return make_api_request(f"Standings/{season}", f"Couldn't fetch team standings for season {season}.")

@st.cache_data(ttl=3600)
def get_player_stats_data(player_id, season):
    """Fetches raw player statistics data for a given player ID and season."""
    return make_api_request(f"PlayerSeasonStatsByPlayerID/{player_id}/{season}", 
                            f"Couldn't fetch stats for player ID {player_id} in {season}.")

@st.cache_data(ttl=86400)
def search_player_data(player_name):
    """Searches for players by name and returns raw player data."""
    data = make_api_request("Players", f"Error searching for player '{player_name}'.")
    if data and isinstance(data, list):
        return [p for p in data if player_name.lower() in p.get('FullName', '').lower()]
    return []

@st.cache_data(ttl=86400)
def get_player_info_data(player_id):
    """Fetches raw detailed information for a specific player by ID."""
    data = make_api_request(f"Player/{player_id}", f"Error fetching info for player ID {player_id}.")
    return data[0] if isinstance(data, list) and len(data) > 0 else (data if isinstance(data, dict) else None)

def render_team_standings(season):
    """Renders MLB team standings for the selected season."""
    st.markdown("---")
    st.header(f"⚾ MLB Team Standings for {season}")
    
    standings = get_team_standings_data(season=season)

    if not standings:
        st.warning(f"No standings data received for {season}. Check your API key and terminal for errors.")
        return

    # Debugging: Print the standings data as it is passed to this function
    print(f"\n[DEBUG] Standings data received by render_team_standings for season {season}:")
    print(json.dumps(standings, indent=2))

    # This part assumes a specific JSON structure from SportsData.io.
    # If the API's response is different, this needs to be adjusted.
    if 'records' not in standings or not standings['records']:
        st.warning(f"Standings data for {season} is missing 'records' key or is empty. API response structure may differ from expected.")
        return

    for record in standings['records']:
        division_name = record.get('division', {}).get('name', "Unknown Division")
        st.subheader(division_name)
        
        teams_data = record.get('teamRecords', [])
        if not teams_data:
            st.info(f"No team records found for {division_name}.")
            continue 

        teams_df = [
            {
                "Team": t.get('team', {}).get('name', 'N/A'),
                "W": t.get('wins', 0),
                "L": t.get('losses', 0),
                "Pct": t.get('winningPercentage', 'N/A'),
                "GB": t.get('gamesBack', 'N/A'),
                "Streak": t.get('streak', {}).get('streakCode', 'N/A'),
            }
            for t in teams_data
        ]
        st.dataframe(teams_df, hide_index=True, use_container_width=True)


def render_player_stats(player_id, season):
    """Renders player statistics for the selected player and season."""
    info = get_player_info_data(player_id)
    if not info:
        st.error(f"No player information found for player ID {player_id}.")
        return

    name = info.get('FullName', 'Unknown Player')
    pos_code = info.get('PrimaryPosition', {}).get('Code', 'N/A')
    st.subheader(f"{name} - {season} Stats")

    stats = get_player_stats_data(player_id, season)
    
    # Ensure 'stats' is a dictionary, handling cases where it might be a list with one item
    if isinstance(stats, list) and len(stats) > 0:
        stats = stats[0]
    elif not isinstance(stats, dict):
        stats = {} 

    if not stats:
        st.info(f"No stats found for {name} in {season}.")
        return
    
    # Debugging: Print the player stats data as it is passed to this function
    print(f"\n[DEBUG] Player stats data received by render_player_stats for player {player_id}, season {season}:")
    print(json.dumps(stats, indent=2))

    col1, col2, col3, col4 = st.columns(4)
    if pos_code == 'P' or info.get('Position', '').upper() == 'P': # Pitcher
        col1.metric("ERA", stats.get('EarnedRunAverage', 'N/A'))
        col2.metric("Wins-Losses", f"{stats.get('Wins', 0)}-{stats.get('Losses', 0)}")
        col3.metric("Strikeouts", stats.get('Strikeouts', 'N/A'))
        col4.metric("WHIP", stats.get('WalksHitsPerInningPitched', 'N/A'))
    else: # Hitter
        col1.metric("AVG", stats.get('BattingAverage', 'N/A'))
        col2.metric("HR", stats.get('HomeRuns', 'N/A'))
        col3.metric("RBI", stats.get('RunsBattedIn', 'N/A'))
        col4.metric("OPS", stats.get('OnBasePlusSlugging', 'N/A'))

def main():
    """Main function to run the Streamlit MLB Stats Viewer application."""
    st.set_page_config(page_title="MLB Stats Viewer", layout="wide")
    st.title("⚾ MLB Stats Viewer")

    current_year = get_current_season_year()
    min_year = 2000
    years = list(range(current_year, min_year - 1, -1))
    
    selected_season_index = years.index(current_year) if current_year in years else 0
    season = st.selectbox("Choose MLB season year:", years, index=selected_season_index)

    if st.button("Refresh Data", help="Clear cached data and refresh."):
        st.cache_data.clear()
        st.experimental_rerun()

    st.session_state.setdefault('search_results', None)
    st.session_state.setdefault('selected_player_id', None)
    st.session_state.selected_season = season

    with st.expander(f"View {season} Team Standings", expanded=True):
        render_team_standings(season=season)

    st.markdown("---")
    st.header("Player Stat Lookup")

    with st.form(key='player_search_form'):
        player_input = st.text_input("Enter player name or MLB ID:", help="Enter full name or numerical MLB Player ID.")
        submit = st.form_submit_button("Search")

    if submit and player_input:
        st.session_state.search_results = None
        st.session_state.selected_player_id = None

        if player_input.isdigit():
            info = get_player_info_data(player_input)
            if info:
                st.session_state.selected_player_id = player_input
            else:
                st.error(f"No player found with ID {player_input}")
        else:
            results = search_player_data(player_input)
            if not results:
                st.warning(f"No players found for '{player_input}'.")
            elif len(results) == 1:
                st.session_state.selected_player_id = results[0].get('PlayerID')
                if not st.session_state.selected_player_id:
                    st.warning(f"Could not retrieve Player ID for {results[0].get('FullName', 'selected player')}.")
            else:
                st.session_state.search_results = results

    if st.session_state.get('search_results'):
        st.subheader("Select a player:")
        player_opts = {
            f"{p.get('FullName', 'N/A')} ({p.get('PrimaryPosition', {}).get('Abbreviation', 'N/A')}, {p.get('Team', 'N/A')})": p.get('PlayerID')
            for p in st.session_state.search_results if p.get('PlayerID')
        }

        if player_opts:
            choice = st.radio("Choose:", list(player_opts.keys()), key="player_choice")
            if choice:
                st.session_state.selected_player_id = player_opts[choice]
                st.session_state.search_results = None
                st.experimental_rerun()
        else:
            st.warning("No selectable players found in search results.")
            st.session_state.search_results = None
            
    elif st.session_state.get('selected_player_id'):
        render_player_stats(st.session_state.selected_player_id, season=season)

if __name__ == "__main__":
    main()
