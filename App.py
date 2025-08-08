import streamlit as st
import requests
import datetime

MLB_API_BASE = "https://sportsdata.io/developers/api-documentation/mlb#standings"

def make_api_request(endpoint, error_msg):
    # TODO: Implement your actual API logic with authentication/key
    # Example placeholder: Replace with requests.get or similar
    # response = requests.get(f"{MLB_API_BASE}/{endpoint}", headers={"Ocp-Apim-Subscription-Key": "YOUR_API_KEY"})
    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     st.error(error_msg)
    #     return {}
    return {}

def get_current_season_year():
    endpoint = "seasons/current"
    data = make_api_request(endpoint, "Couldn't fetch current MLB season.")
    if data and 'seasonId' in data:
        try:
            return int(data['seasonId'])
        except Exception:
            pass
    return datetime.datetime.now().year

@st.cache_data(ttl=3600)
def get_team_standings(season, league_ids="103,104"):
    endpoint = f"standings?leagueId={league_ids}&season={season}"
    return make_api_request(endpoint, "Couldn't fetch team standings.")

@st.cache_data(ttl=3600)
def get_player_stats(player_id, season):
    endpoint = f"people/{player_id}/stats?stats=season&season={season}"
    return make_api_request(endpoint, f"Couldn't fetch stats for player ID {player_id}.")

@st.cache_data(ttl=86400)
def search_player(player_name):
    endpoint = f"people/search?names={player_name}"
    data = make_api_request(endpoint, f"Error searching for player '{player_name}'.")
    return data.get('people', []) if data else []

@st.cache_data(ttl=86400)
def get_player_info(player_id):
    endpoint = f"people/{player_id}"
    data = make_api_request(endpoint, f"Error fetching info for player ID {player_id}.")
    return data['people'][0] if data and data.get('people') else None

def render_team_standings(season):
    standings = get_team_standings(season=season)
    if not standings or 'records' not in standings:
        st.warning("No team standings available.")
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
        st.dataframe(teams, hide_index=True, use_container_width=True)

def render_player_stats(player_id, season):
    info = get_player_info(player_id)
    if not info:
        st.error(f"No info found for player ID {player_id}")
        return

    name = info.get('fullName', 'Unknown Player')
    pos_code = info.get('primaryPosition', {}).get('code', 'N/A')
    st.subheader(f"{name} - {season} Stats")

    stats_data = get_player_stats(player_id, season)
    stats = (
        stats_data.get('stats', [{}])[0]
        .get('splits', [{}])[0]
        .get('stat', {})
        if stats_data and stats_data.get('stats') else {}
    )

    if stats:
        if pos_code == '1':  # Pitcher
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("ERA", stats.get('era', 'N/A'))
            col2.metric("Wins-Losses", f"{stats.get('wins', 0)}-{stats.get('losses', 0)}")
            col3.metric("Strikeouts", stats.get('strikeOuts', 'N/A'))
            col4.metric("WHIP", stats.get('whip', 'N/A'))
        else:  # Hitter
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("AVG", stats.get('avg', 'N/A'))
            col2.metric("HR", stats.get('homeRuns', 'N/A'))
            col3.metric("RBI", stats.get('rbi', 'N/A'))
            col4.metric("OPS", stats.get('ops', 'N/A'))
    else:
        st.info(f"No stats found for {name} in {season}.")

def main():
    st.set_page_config(page_title="MLB Stats Viewer", layout="wide")
    st.title("⚾ MLB Stats Viewer")

    # Dynamically get the most current year
    current_year = get_current_season_year()
    min_year = 2000
    years = list(range(current_year, min_year - 1, -1))
    season = st.selectbox("Choose MLB season year:", years, index=0)

    # Add a refresh button
    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.experimental_rerun()

    # Session state management
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
                st.session_state.selected_player_id = results[0].get('id')
            else:
                st.session_state.search_results = results

    # If multiple players found, prompt user to choose
    if st.session_state.get('search_results'):
        st.subheader("Select a player:")
        player_opts = {
            f"{p.get('fullName', 'N/A')} ({p.get('primaryPosition', {}).get('abbreviation', 'N/A')}, {p.get('currentTeam', {}).get('name', 'N/A')})": p.get('id')
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
