import streamlit as st
import requests
import datetime

# Base URL for the SportsData.io MLB API
# Note: The original link provided in the comments was for API documentation.
# You'll need the actual base URL for the API endpoints, which typically looks like this:
MLB_API_BASE = "https://api.sportsdata.io/v3/mlb/scores/json" # This is a common pattern, verify with SportsData.io documentation
# Replace "YOUR_API_KEY" with your actual SportsData.io subscription key.
API_KEY = "3031838cee374a47a9ccac67652ae731"

def make_api_request(endpoint, error_msg):
    """
    Makes a GET request to the SportsData.io MLB API.
    Args:
        endpoint (str): The specific API endpoint to call (e.g., "Standings/2023").
        error_msg (str): The message to display if the API request fails.
    Returns:
        dict: The JSON response from the API, or an empty dictionary if an error occurs.
    """
    if API_KEY == "YOUR_API_KEY":
        st.error("Please replace 'YOUR_API_KEY' with your actual SportsData.io API key.")
        return {}

    try:
        # Construct the full API URL. Make sure the endpoint matches what the API expects.
        # For SportsData.io, endpoints often look like 'Standings/2023', 'Players', etc.
        # Check their documentation for the exact paths.
        url = f"{MLB_API_BASE}/{endpoint}?key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"{error_msg} (HTTP Error: {e.response.status_code}) - Check API key and endpoint.")
        return {}
    except requests.exceptions.ConnectionError:
        st.error(f"{error_msg} (Connection Error) - Check your internet connection.")
        return {}
    except requests.exceptions.Timeout:
        st.error(f"{error_msg} (Timeout Error) - The request took too long.")
        return {}
    except requests.exceptions.RequestException as e:
        st.error(f"{error_msg} (An unexpected error occurred: {e})")
        return {}

def get_current_season_year():
    """
    Determines the current MLB season year.
    Attempts to fetch from API, falls back to current calendar year if API fails.
    Note: SportsData.io might have a specific endpoint for 'current season'.
    A common pattern is 'CurrentSeason'. Verify with API documentation.
    For this example, we'll assume 'CurrentSeason' returns an object with a 'Season' field.
    """
    # Example endpoint for current season. This might vary based on the actual API structure.
    # A common SportsData.io endpoint might be "CurrentSeason" or similar to get the active season.
    endpoint = "CurrentSeason" # This is a hypothetical endpoint, adjust based on actual API
    data = make_api_request(endpoint, "Couldn't fetch current MLB season from API.")
    if data and 'Season' in data: # Assuming the API returns a 'Season' field for the current season
        try:
            return int(data['Season'])
        except ValueError:
            st.warning("Could not parse current season year from API response. Using current calendar year.")
            return datetime.datetime.now().year
    else:
        st.info("Falling back to current calendar year as API did not provide current season.")
        return datetime.datetime.now().year

@st.cache_data(ttl=3600)
def get_team_standings(season, league_ids="103,104"):
    """
    Fetches team standings for a given season and league IDs.
    Note: SportsData.io often uses endpoints like 'Standings/{season_year}'.
    The 'leagueId' parameter might need to be passed differently or be part of the base URL
    depending on their API design. This example assumes a query parameter.
    """
    # Assuming an endpoint like 'Standings/{season}' where leagueId is a query param
    endpoint = f"Standings/{season}" # Common pattern, verify with SportsData.io documentation
    # SportsData.io API might not use 'leagueId' directly in this way.
    # You might need to filter results after getting all standings for a season,
    # or the API might have different endpoints for AL/NL standings.
    return make_api_request(endpoint, f"Couldn't fetch team standings for season {season}.")

@st.cache_data(ttl=3600)
def get_player_stats(player_id, season):
    """
    Fetches player statistics for a given player ID and season.
    Note: SportsData.io player stats endpoints are typically like 'PlayerSeasonStatsByPlayerID/{player_id}/{season}'.
    """
    # Common pattern for player stats, verify with SportsData.io documentation
    endpoint = f"PlayerSeasonStatsByPlayerID/{player_id}/{season}"
    return make_api_request(endpoint, f"Couldn't fetch stats for player ID {player_id} in {season}.")

@st.cache_data(ttl=86400)
def search_player(player_name):
    """
    Searches for players by name.
    Note: SportsData.io might have a 'Players' endpoint with a search query parameter,
    e.g., 'Players?name={player_name}'.
    """
    # Common pattern for player search, verify with SportsData.io documentation
    endpoint = f"Players" # Assuming 'Players' endpoint returns all players
    # Then filter by name on the client side, or if API supports:
    # endpoint = f"Players?search={player_name}" # If API has a search param
    data = make_api_request(endpoint, f"Error searching for player '{player_name}'.")
    # If the API returns a list of players and you need to filter:
    if data and isinstance(data, list):
        # Filter on client-side if API doesn't support direct name search param
        return [p for p in data if player_name.lower() in p.get('FullName', '').lower()]
    return [] # Return empty list if no data or data not in expected format

@st.cache_data(ttl=86400)
def get_player_info(player_id):
    """
    Fetches detailed information for a specific player by ID.
    Note: SportsData.io often uses 'Player/{player_id}'.
    """
    endpoint = f"Player/{player_id}" # Common pattern, verify with SportsData.io documentation
    data = make_api_request(endpoint, f"Error fetching info for player ID {player_id}.")
    # Assuming the API returns a single player object directly or a list with one player
    if data and isinstance(data, dict):
        return data
    elif data and isinstance(data, list) and len(data) > 0:
        return data[0]
    return None

def render_team_standings(season):
    """Renders MLB team standings for the selected season."""
    st.markdown("---") # Add a horizontal rule for separation
    st.header(f"⚾ MLB Team Standings for {season}")
    # The API might return standings broken down by League/Division,
    # or just a flat list. This code assumes a 'records' key,
    # and then 'division' and 'teamRecords' within each record.
    # You might need to adjust the parsing logic based on the actual API response structure.
    standings = get_team_standings(season=season)

    if not standings:
        st.warning("Could not load team standings. Please check API key and endpoint configuration.")
        return

    # Assuming the structure is a list of division records directly if API returns flat list,
    # or an outer dict with a 'Records' key. Adjust as per actual API response.
    # For SportsData.io, standings often come as a list of teams with division info inside.
    
    # Placeholder for actual parsing based on SportsData.io Standings API response structure.
    # Example: if API returns a list of teams, each with 'Division', 'TeamName', 'Wins', 'Losses'
    
    # This part requires a careful check of the actual SportsData.io API response for Standings.
    # The original code's structure for 'standings['records']' and 'record.get('division')'
    # suggests a nested structure, which might not directly match SportsData.io's typical flat list of teams.
    # I'll create a simplified mock structure if the actual data is not available to test.
    
    # If the API returns a list of records, where each record has 'DivisionName' and 'TeamRecords'
    # If it's a flat list of team objects, you'd group them by division.
    
    # For now, I'll adapt to a common SportsData.io pattern where standings for a season might return
    # a flat list of team records, and you group them by division.
    
    # This part is highly dependent on the actual JSON structure from SportsData.io
    # For demonstration, let's assume get_team_standings returns a list of dictionaries,
    # where each dict represents a team's standing and includes 'Division' and 'League'.
    
    # Mock data structure if actual API call fails:
    # standings_data = [
    #     {"Division": "AL East", "TeamName": "Yankees", "Wins": 100, "Losses": 62, "WinningPercentage": 0.617, "GamesBack": 0, "StreakCode": "W5"},
    #     {"Division": "AL East", "TeamName": "Red Sox", "Wins": 85, "Losses": 77, "WinningPercentage": 0.525, "GamesBack": 15, "StreakCode": "L2"},
    #     {"Division": "NL West", "TeamName": "Dodgers", "Wins": 110, "Losses": 52, "WinningPercentage": 0.679, "GamesBack": 0, "StreakCode": "W7"},
    # ]
    # You'd need to adapt the rendering logic below based on the actual 'standings' variable content.

    # Simplified rendering assuming a flat list of team records directly from the API,
    # and then grouping them for display.
    # The original code's 'records' structure suggests an API that provides nested divisions.
    # Let's keep the original parsing but add a warning if 'records' isn't found.

    if 'records' not in standings or not standings['records']:
        st.warning(f"No detailed standings data found for {season}. Please check the API response structure.")
        # As a fallback, try to render if it's just a flat list of teams directly under 'standings'
        if isinstance(standings, list) and len(standings) > 0 and 'TeamName' in standings[0]:
            st.subheader("All Teams (Ungrouped)")
            teams = [
                {
                    "Team": t.get('TeamName', 'N/A'),
                    "W": t.get('Wins', 0),
                    "L": t.get('Losses', 0),
                    "Pct": t.get('WinningPercentage', 'N/A'),
                    "GB": t.get('GamesBack', 'N/A'),
                    "Streak": t.get('Streak', {}).get('StreakCode', 'N/A'), # Assuming streak might be nested
                }
                for t in standings
            ]
            st.dataframe(teams, hide_index=True, use_container_width=True)
        return

    for record in standings['records']:
        division_name = record.get('division', {}).get('name', "Unknown Division")
        st.subheader(division_name)
        teams = [
            {
                "Team": t.get('team', {}).get('name', 'N/A'),
                "W": t.get('wins', 0),
                "L": t.get('losses', 0),
                "Pct": t.get('winningPercentage', 'N/A'),
                "GB": t.get('gamesBack', 'N/A'),
                "Streak": t.get('streak', {}).get('streakCode', 'N/A'),
            }
            for t in record.get('teamRecords', [])
        ]
        if teams:
            st.dataframe(teams, hide_index=True, use_container_width=True)
        else:
            st.info(f"No team records found for {division_name}.")


def render_player_stats(player_id, season):
    """Renders player statistics for the selected player and season."""
    info = get_player_info(player_id)
    if not info:
        st.error(f"No player information found for player ID {player_id}.")
        return

    name = info.get('FullName', 'Unknown Player') # SportsData.io often uses 'FullName'
    pos_code = info.get('PrimaryPosition', {}).get('Code', 'N/A') # SportsData.io often uses 'PrimaryPosition' with 'Code'
    st.subheader(f"{name} - {season} Stats")

    stats_data = get_player_stats(player_id, season)
    
    # SportsData.io API for player season stats usually returns a single object directly,
    # or a list containing one object if the endpoint returns a list.
    # The original parsing seems to assume a very specific nested structure ('stats', 'splits', 'stat').
    # I'll adjust this to a more common SportsData.io structure for season stats.
    
    stats = {}
    if isinstance(stats_data, dict):
        stats = stats_data # Assume direct stat object
    elif isinstance(stats_data, list) and len(stats_data) > 0:
        stats = stats_data[0] # Assume list containing the stat object

    if stats:
        # Check if the player is a pitcher based on position code.
        # Common pitcher codes include 'P' or numeric codes specific to the API.
        # Assuming 'P' for Pitcher, 'B' for Batter. Adjust `pos_code` check if different.
        if pos_code == 'P' or info.get('Position', '').upper() == 'P':  # Assuming 'P' for pitcher, check both codes and a potential 'Position' field
            col1, col2, col3, col4 = st.columns(4)
            # SportsData.io often uses specific keys like 'EarnedRunAverage', 'Wins', 'Losses', 'Strikeouts', 'WalksHitsPerInningPitched'
            col1.metric("ERA", stats.get('EarnedRunAverage', 'N/A'))
            col2.metric("Wins-Losses", f"{stats.get('Wins', 0)}-{stats.get('Losses', 0)}")
            col3.metric("Strikeouts", stats.get('Strikeouts', 'N/A'))
            col4.metric("WHIP", stats.get('WalksHitsPerInningPitched', 'N/A'))
        else:  # Hitter
            col1, col2, col3, col4 = st.columns(4)
            # SportsData.io often uses specific keys like 'BattingAverage', 'HomeRuns', 'RunsBattedIn', 'OnBasePlusSlugging'
            col1.metric("AVG", stats.get('BattingAverage', 'N/A'))
            col2.metric("HR", stats.get('HomeRuns', 'N/A'))
            col3.metric("RBI", stats.get('RunsBattedIn', 'N/A'))
            col4.metric("OPS", stats.get('OnBasePlusSlugging', 'N/A'))
    else:
        st.info(f"No stats found for {name} in {season}.")

def main():
    """Main function to run the Streamlit MLB Stats Viewer application."""
    st.set_page_config(page_title="MLB Stats Viewer", layout="wide")
    st.title("⚾ MLB Stats Viewer")

    # Dynamically get the most current year
    # Adjust `min_year` as needed based on how far back SportsData.io API provides data.
    current_year = get_current_season_year()
    min_year = 2000
    years = list(range(current_year, min_year - 1, -1))
    
    # Ensure the default `index` is valid for the `years` list.
    # If current_year is less than 2000, this could cause an error.
    selected_season_index = years.index(current_year) if current_year in years else 0
    season = st.selectbox("Choose MLB season year:", years, index=selected_season_index)


    # Add a refresh button to clear cache
    if st.button("Refresh Data", help="Clear cached data and refresh."):
        st.cache_data.clear()
        st.experimental_rerun()

    # Session state management for player search results and selection
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'selected_player_id' not in st.session_state:
        st.session_state.selected_player_id = None
    if 'selected_season' not in st.session_state:
        st.session_state.selected_season = season
    else:
        st.session_state.selected_season = season # Update selected season if changed

    # Display Team Standings
    with st.expander(f"View {season} Team Standings", expanded=True):
        render_team_standings(season=season)

    st.markdown("---")
    st.header("Player Stat Lookup")

    # Player search form
    with st.form(key='player_search_form'):
        player_input = st.text_input("Enter player name or MLB ID:", help="Enter full name or numerical MLB Player ID.")
        submit = st.form_submit_button("Search")

    if submit and player_input:
        st.session_state.search_results = None
        st.session_state.selected_player_id = None

        if player_input.isdigit():
            info = get_player_info(player_input)
            if info:
                st.session_state.selected_player_id = player_input
            else:
                st.error(f"No player found with ID {player_input}")
        else:
            results = search_player(player_input)
            if not results:
                st.warning(f"No players found for '{player_input}'.")
            elif len(results) == 1:
                # SportsData.io often uses 'PlayerID' for the ID.
                st.session_state.selected_player_id = results[0].get('PlayerID')
                if not st.session_state.selected_player_id:
                    st.warning(f"Could not retrieve Player ID for {results[0].get('FullName', 'selected player')}.")
            else:
                st.session_state.search_results = results

    # If multiple players found, prompt user to choose
    if st.session_state.get('search_results'):
        st.subheader("Select a player:")
        player_opts = {}
        for p in st.session_state.search_results:
            # SportsData.io uses 'FullName', 'PrimaryPosition', 'Team' (Team Name)
            full_name = p.get('FullName', 'N/A')
            pos_abbr = p.get('PrimaryPosition', {}).get('Abbreviation', 'N/A') # Assuming PrimaryPosition is a dict
            team_name = p.get('Team', 'N/A') # Assuming 'Team' directly gives the team name
            player_id = p.get('PlayerID') # The actual ID to use for fetching stats

            if player_id: # Only add valid players with an ID
                option_label = f"{full_name} ({pos_abbr}, {team_name})"
                player_opts[option_label] = player_id

        if player_opts:
            choice = st.radio("Choose:", list(player_opts.keys()), key="player_choice")
            if choice:
                st.session_state.selected_player_id = player_opts[choice]
                st.session_state.search_results = None # Clear search results after selection
                st.experimental_rerun() # Rerun to display stats for the selected player
        else:
            st.warning("No selectable players found in search results.")
            st.session_state.search_results = None # Clear search results if none are valid
            
    # Display stats if a player is selected
    elif st.session_state.get('selected_player_id'):
        render_player_stats(st.session_state.selected_player_id, season=season)

if __name__ == "__main__":
    main()
