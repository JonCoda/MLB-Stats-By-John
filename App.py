import streamlit as st
import requests

API_BASE = "https://sportsdata.io/developers/api-documentation/mlb"

def api_get(endpoint, error_msg):
    """Unified GET request with error handling."""
    try:
        resp = requests.get(endpoint)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"{error_msg}: {e}")
        return None

@st.cache_data(ttl=3600)
def get_standings(season="2024", league="103,104"):
    url = f"{API_BASE}/standings?leagueId={league}&season={season}"
    return api_get(url, "Failed to fetch standings")

@st.cache_data(ttl=3600)
def get_stats(pid, season="2024"):
    url = f"{API_BASE}/people/{pid}/stats?stats=season&season={season}"
    return api_get(url, "Failed to fetch player stats")

@st.cache_data(ttl=86400)
def search_player(name):
    url = f"{API_BASE}/people/search?names={name}"
    data = api_get(url, f"Player search error: {name}")
    return data.get('people', []) if data else []

@st.cache_data(ttl=86400)
def get_player(pid):
    url = f"{API_BASE}/people/{pid}"
    data = api_get(url, f"Player info error: {pid}")
    return (data.get('people') or [None])[0]

def show_standings(season="2024"):
    data = get_standings(season)
    if not data or 'records' not in data:
        st.warning("Could not retrieve standings.")
        return
    for record in data['records']:
        st.subheader(record['division']['name'])
        teams = [
            {
                "Team": t['team']['name'],
                "W": t['wins'],
                "L": t['losses'],
                "Pct": t.get('winningPercentage', '.000'),
                "GB": t.get('gamesBack', '-'),
                "Streak": t.get('streak', {}).get('streakCode', '-')
            }
            for t in record.get('teamRecords', [])
        ]
        st.table(teams if teams else [{"Team": "No data"}])

def show_player_stats(pid, season="2024"):
    info = get_player(pid)
    if not info:
        st.error(f"Could not retrieve player {pid}")
        return
    st.subheader(f"{info.get('fullName', 'Unknown')}: {season} Stats")
    stats = get_stats(pid, season)
    splits = (stats or {}).get('stats', [{}])[0].get('splits', [])
    if splits:
        s = splits[0]['stat']
        cols = st.columns(4)
        metrics = [("Batting Avg", s.get('avg')), ("Home Runs", s.get('homeRuns')), ("RBIs", s.get('rbi')), ("OPS", s.get('ops'))]
        for col, (label, val) in zip(cols, metrics):
            col.metric(label, val or 'N/A')
    else:
        st.info(f"No {season} stats for {info.get('fullName', '')}")

def main():
    st.title("MLB Stats")
    menu = ["Team Standings", "Player Search"]
    choice = st.sidebar.radio("Select View", menu)

    if choice == "Team Standings":
        season = st.sidebar.text_input("Season", "2024")
        show_standings(season)
    else:
        name_or_id = st.text_input("Player Name or ID")
        if name_or_id:
            if name_or_id.isdigit():
                pid = name_or_id
            else:
                results = search_player(name_or_id)
                if not results:
                    st.error("No matching players.")
                    return
                if len(results) == 1:
                    pid = results[0]['id']
                else:
                    st.write("Select a player:")
                    pid = st.selectbox("Players", results, format_func=lambda p: f"{p['fullName']} ({p['id']})")['id']
            show_player_stats(pid)

if __name__ == "__main__":
    main()
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
