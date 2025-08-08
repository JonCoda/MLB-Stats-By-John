import streamlit as st
import requests
import datetime

# Correct SportsData.io MLB API base URL
MLB_API_BASE = "https://api.sportsdata.io/v4/mlb/scores/json"
API_KEY = "YOUR_API_KEY"  # <-- Replace with your real API key

HEADERS = {"Ocp-Apim-Subscription-Key": API_KEY}

def get_current_season_year():
    # SportsData.io does not provide a "current season" endpoint;
    # fallback to current year, or use get_all_seasons and pick the latest
    try:
        seasons = make_api_request("Seasons", "Couldn't fetch MLB seasons.")
        if seasons:
            # Each season entry has 'Season' field (int year)
            return max(season['Season'] for season in seasons if 'Season' in season)
    except Exception:
        pass
    return datetime.datetime.now().year
        
def make_api_request(endpoint, error_message):
    url = f"{MLB_API_BASE}/{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"{error_message}: {e}")
        return None
        
@st.cache_data(ttl=3600)
def get_team_standings(season):
    # SportsData.io endpoint: Standings/{season}
    endpoint = f"Standings/{season}"
    return make_api_request(endpoint, "Couldn't fetch team standings.")

@st.cache_data(ttl=3600)
def get_player_stats(player_id, season):
    # SportsData.io endpoint: PlayerSeasonStatsByPlayer/{season}/{playerid}
    endpoint = f"PlayerSeasonStatsByPlayer/{season}/{player_id}"
    data = make_api_request(endpoint, f"Couldn't fetch stats for player ID {player_id}.")
    return data[0] if data else {}  # Returns a list

@st.cache_data(ttl=86400)
def search_player(player_name):
    # SportsData.io does not have a direct "search" endpoint.
    # Instead, get all players and search by name client-side.
    players = make_api_request("Players", "Error fetching players list.")
    name_lower = player_name.lower()
    matches = [
        p for p in players if name_lower in p.get("FirstName", "").lower() or name_lower in p.get("LastName", "").lower()
    ]
    return matches

@st.cache_data(ttl=86400)
def get_player_info(player_id):
    # SportsData.io endpoint: Player/{playerid}
    endpoint = f"Player/{player_id}"
    return make_api_request(endpoint, f"Error fetching info for player ID {player_id}.")

def render_team_standings(season):
    standings = get_team_standings(season=season)
    if not standings:
        st.warning("No team standings available.")
        return

    # Standings is a list of team dicts
    teams = [
        {
            "Team": t.get('Name', 'N/A'),
            "W": t.get('Wins', 0),
            "L": t.get('Losses', 0),
            "Pct": t.get('Percentage', 'N/A'),
            "GB": t.get('GamesBack', 'N/A'),
            "Streak": t.get('Streak', 'N/A'),
            "Division": t.get('Division', 'N/A')
        }
        for t in standings
    ]
    # Group by division
    divisions = {}
    for team in teams:
        div = team["Division"]
        divisions.setdefault(div, []).append(team)
    for div, team_list in divisions.items():
        st.subheader(div)
        st.dataframe(team_list, hide_index=True, use_container_width=True)

def render_player_stats(player_id, season):
    info = get_player_info(player_id)
    if not info:
        st.error(f"No info found for player ID {player_id}")
        return
    name = f"{info.get('FirstName', '')} {info.get('LastName', '')}".strip()
    pos_code = info.get('Position', 'N/A')
    st.subheader(f"{name} - {season} Stats")

    stats = get_player_stats(player_id, season)
    if stats:
        if pos_code == 'P':  # Pitcher
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("ERA", stats.get('EarnedRunAverage', 'N/A'))
            col2.metric("Wins-Losses", f"{stats.get('Wins', 0)}-{stats.get('Losses', 0)}")
            col3.metric("Strikeouts", stats.get('Strikeouts', 'N/A'))
            col4.metric("WHIP", stats.get('WalksHitsPerInningsPitched', 'N/A'))
        else:  # Hitter
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("AVG", stats.get('BattingAverage', 'N/A'))
            col2.metric("HR", stats.get('HomeRuns', 'N/A'))
            col3.metric("RBI", stats.get('RunsBattedIn', 'N/A'))
            col4.metric("OPS", stats.get('OnBasePlusSlugging', 'N/A'))
    else:
        st.info(f"No stats found for {name} in {season}.")

def main():
    st.set_page_config(page_title="MLB Stats Viewer", layout="wide")
    st.title("⚾ MLB Stats Viewer")
    
    current_year = get_current_season_year()
    min_year = 2000
    years = list(range(current_year, min_year - 1, -1))
    season = st.selectbox("Choose MLB season year:", years, index=0)

    search_results = st.session_state.get('search_results')
    selected_player = st.session_state.get('selected_player_id')
    selected_season = st.session_state.get('selected_season', season)
    st.session_state.selected_season = season

    with st.expander(f"View {season} Team Standings", expanded=True):
        render_team_standings(season=season)

    st.divider()
    st.header("Player Stat Lookup")

    with st.form(key='player_search_form'):
        player_input = st.text_input("Enter player name or MLB ID:")
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
                    st.session_state.selected_player_id = results[0].get('PlayerID')
                else:
                    st.session_state.search_results = results

    if st.session_state.get('search_results'):
        st.subheader("Select a player:")
        player_opts = {
            f"{p.get('FirstName', 'N/A')} {p.get('LastName', 'N/A')} ({p.get('Position', 'N/A')}, {p.get('Team', 'N/A')})": p.get('PlayerID')
            for p in st.session_state.search_results
        }
        choice = st.radio("Choose:", list(player_opts.keys()), key="player_choice")
        if choice:
            st.session_state.selected_player_id = player_opts[choice]
            st.session_state.search_results = None
            st.experimental_rerun()
    elif st.session_state.get('selected_player_id'):
        render_player_stats(st.session_state.selected_player_id, season=season)

if __name__ == "__main__":
    main()
