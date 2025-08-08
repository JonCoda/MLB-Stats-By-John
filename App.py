import streamlit as st
import requests

class MLBApi:
    BASE_URL = "https://statsapi.mlb.com/api/v1"

    def get_team_standings(self, season="2025"):
        url = f"{self.BASE_URL}/standings?season={season}&leagueId=103,104"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch team standings: {e}")
            return None

    def get_player_stats(self, player_id, season="2024"):
        url = f"{self.BASE_URL}/people/{player_id}/stats?stats=season&season={season}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch player stats: {e}")
            return None

    def find_player(self, player_name):
        url = f"{self.BASE_URL}/people/search?names={player_name}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('people', [])
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to search for player: {e}")
            return []

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
