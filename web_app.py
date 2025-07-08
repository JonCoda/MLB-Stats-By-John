import streamlit as st
from streamlit_autorefresh import st_autorefres 
from MLBDeepDive import find_team, find_players
from LiveScores import datetime 
import requests

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MLB Stats Finder",
    page_icon="⚾",
    layout="centered",
)

# --- SIDEBAR: MLB ADVANCED STATS ---
def get_advanced_stats(player_name):
    # Implement your real advanced stat fetching logic here
    # Remove or replace this function if not needed
    return None  # Remove this line after implementing

st.sidebar.header("MLB Advanced Stats")
adv_player = st.sidebar.text_input(
    "Enter player name for advanced stats:",
    placeholder="e.g. Mookie Betts",
    key="adv_stats_player"
)

if adv_player:
    with st.sidebar:
        with st.spinner("Fetching advanced stats..."):
            adv_stats = get_advanced_stats(adv_player)
        if adv_stats:
            st.success(f"Advanced Stats for {adv_player}")
            for stat_name, stat_value in adv_stats.items():
                st.write(f"**{stat_name}:** {stat_value}")
        else:
            st.warning("Player not found or stats unavailable.")
else:
    st.sidebar.markdown("Enter a player name to view advanced stats such as OPS, WAR, WHIP, and more.")

# --- SIDEBAR: LIVE SCORE TICKER TOGGLE ---
show_ticker = st.sidebar.checkbox("Show Live Score Ticker")

# --- MAIN HEADER ---
st.title("⚾ MLB Stats Finder")
st.write("Search for information about your favorite MLB teams and players.")

# --- LIVE SCORE TICKER ---
def get_scores():
    url = "http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    try:
        response = requests.get(url, timeout=7)
        data = response.json()
        games = data.get('events', [])
        scores = []
        for game in games:
            competition = game['competitions'][0]
            status = competition['status']['type']['description']
            teams = competition['competitors']
            home = next(team for team in teams if team['homeAway'] == 'home')
            away = next(team for team in teams if team['homeAway'] == 'away')
            scores.append({
                "matchup": f"{away['team']['displayName']} @ {home['team']['displayName']}",
                "score": f"{away['score']} - {home['score']}",
                "status": status
            })
        return scores
    except Exception:
        return None

if show_ticker:
    st_autorefresh(interval=30_000, key="tickerrefresh")  # Refreshes every 30 seconds
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=30_000, key="tickerrefresh")
    except ImportError:
        st.info("Install `streamlit-autorefresh` for auto refresh.")
    st.subheader("MLB Live Score Ticker")
    scores = get_scores()
    if scores is None:
        st.warning("Could not fetch live scores at this time.")
    elif not scores:
        st.write("No games found.")
    else:
        for s in scores:
            st.write(f"**{s['matchup']}**: {s['score']} ({s['status']})")

# --- MAIN SEARCH UI ---
search_type = st.radio(
    "What do you want to search for?",
    ('Team', 'Player'),
    horizontal=True
)

if search_type == 'Team':
    team_name = st.text_input("Enter the MLB team name:", placeholder="e.g., Boston Red Sox")
    if st.button("Search for Team"):
        if not team_name:
            st.warning("Please enter a team name.")
        else:
            with st.spinner(f"Searching for '{team_name}'..."):
                found_team_data = find_team(team_name)
            if found_team_data:
                st.success(f"Found information for **{found_team_data.get('name')}**!")
                st.subheader("Team Information")
                st.markdown(f"""
                - **Location:** {found_team_data.get('locationName')}
                - **Division:** {found_team_data.get('division', {}).get('name')}
                - **League:** {found_team_data.get('league', {}).get('name')}
                - **Venue:** {found_team_data.get('venue', {}).get('name')}
                - **Team ID:** {found_team_data.get('id')}
                """)
            else:
                st.error(f"Team '{team_name}' not found. Please check the name and try again.")

elif search_type == 'Player':
    player_name = st.text_input("Enter the MLB player name:", placeholder="e.g., Shohei Ohtani")
    if st.button("Search for Player"):
        if not player_name:
            st.warning("Please enter a player name.")
        else:
            with st.spinner(f"Searching for '{player_name}'..."):
                players_found = find_players(player_name)
            if players_found is None:
                st.error("An error occurred while fetching player data. The MLB API might be down.")
            elif len(players_found) == 1:
                player = players_found[0]
                st.success(f"Found information for **{player.get('fullName')}**!")
                st.subheader("Player Information")
                st.markdown(f"""
                - **Primary Position:** {player.get('primaryPosition', {}).get('name', 'N/A')}
                - **Current Team:** {player.get('currentTeam', {}).get('name', 'N/A')}
                - **Player ID:** {player.get('id')}
                """)
            elif len(players_found) > 1:
                st.info(f"Found multiple players for '{player_name}'.")
                st.write("Possible matches:")
                for player in players_found:
                    team_name = player.get('currentTeam', {}).get('name', 'N/A')
                    st.markdown(f"- {player.get('fullName')} ({team_name})")
            else:
                st.error(f"Player '{player_name}' not found. Please check the spelling.")