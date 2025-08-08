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
