import streamlit as st
import requests
import json

class MLBApi:
    BASE_URL = "https://statsapi.mlb.com/api/v1"

    def _make_request(self, url, error_message):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"{error_message}: {e}")
            return None
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse API response. The data may not be in the expected format. Error: {e}")
            return None

    @st.cache_data(ttl=3600)
    def get_team_standings(self, season="2024", league_ids="103,104"):
        url = f"{self.BASE_URL}/standings?leagueId={league_ids}&season={season}"
        return self._make_request(url, f"Failed to fetch team standings for season {season}")

    @st.cache_data(ttl=3600)
    def get_player_stats(self, player_id, season="2024"):
        url = f"{self.BASE_URL}/people/{player_id}/stats?stats=season&season={season}"
        return self._make_request(url, f"Failed to fetch stats for player ID {player_id}")

    @st.cache_data(ttl=86400)
    def find_player(self, player_name):
        url = f"{self.BASE_URL}/people/search?names={player_name}"
        data = self._make_request(url, f"Error searching for player '{player_name}'")
        return data.get('people', []) if data else None

    @st.cache_data(ttl=86400)
    def get_player_info(self, player_id):
        url = f"{self.BASE_URL}/people/{player_id}"
        data = self._make_request(url, f"Error fetching info for player ID '{player_id}'")
        return data['people'][0] if data and data.get('people') else None

def display_team_standings(api, season="2024"):
    data = api.get_team_standings(season=season)
    if not data or 'records' not in data:
        st.warning("Could not retrieve team standings at the moment.")
        return

    for record in data.get('records', []):
        division = record.get('division', {})
        division_name = division.get('name', "Unknown Division")
        st.subheader(division_name)

        team_records = record.get('teamRecords', [])
        if not team_records:
            st.write("No team records found for this division.")
            continue

        # Build the standings table robustly
        team_data = []
        for team in team_records:
            team_info = team.get('team', {})
            team_data.append({
                "Team": team_info.get('name', 'N/A'),
                "W": team.get('wins', 0),
                "L": team.get('losses', 0),
                "Pct": team.get('winningPercentage', '.000'),
                "GB": team.get('gamesBack', '-'),
                "Streak": team.get('streak', {}).get('streakCode', '-')
            })

        # Display using Streamlit's dataframe
        st.dataframe(team_data, hide_index=True, use_container_width=True)

def display_player_stats(api, player_id, season="2024"):
    player_info = api.get_player_info(player_id)
    if not player_info:
        st.error(f"Could not retrieve information for player ID {player_id}.")
        return

    player_name = player_info.get('fullName', 'Unknown Player')
    position = player_info.get('primaryPosition', {}).get('code', 'N/A')
    st.subheader(f"Season Stats for {player_name}")

    data = api.get_player_stats(player_id, season=season)
    try:
        stats = data['stats'][0]['splits'][0]['stat']
    except (AttributeError, IndexError, KeyError, TypeError):
        stats = None

    if stats:
        if position == '1':
            col1, col2, col3, col4 = st.columns(4)
            win_loss = f"{stats.get('wins', 0)}-{stats.get('losses', 0)}"
            col1.metric("ERA", stats.get('era', 'N/A'))
            col2.metric("W-L", win_loss)
            col3.metric("Strikeouts", stats.get('strikeOuts', 'N/A'))
            col4.metric("WHIP", stats.get('whip', 'N/A'))
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Batting Avg", stats.get('avg', 'N/A'))
            col2.metric("Home Runs", stats.get('homeRuns', 'N/A'))
            col3.metric("RBIs", stats.get('rbi', 'N/A'))
            col4.metric("OPS", stats.get('ops', 'N/A'))
    else:
        st.info(f"No {season} stats found for {player_name} (ID: {player_id}). They may not have played this season.")

def main():
    st.set_page_config(page_title="MLB Stats Viewer", layout="wide")
    st.title("⚾ MLB Stats Viewer")

    # Initialize session state keys if not set
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'selected_player_id' not in st.session_state:
        st.session_state.selected_player_id = None

    api = MLBApi()

    with st.expander("View 2024 Team Standings", expanded=True):
        display_team_standings(api)

    st.divider()

    st.header("Player Stat Lookup")
    with st.form(key='player_search_form'):
        player_input = st.text_input("Enter a player name or ID (e.g., 'Aaron Judge', '660271')")
        submit_button = st.form_submit_button(label='Search')

        if submit_button and player_input:
            st.session_state.search_results = None
            st.session_state.selected_player_id = None

            if player_input.isdigit():
                if api.get_player_info(player_input):
                    st.session_state.selected_player_id = player_input
                else:
                    st.error(f"No player found with ID {player_input}.")
            else:
                results = api.find_player(player_input)
                if not results:
                    st.warning(f"No players found matching '{player_input}'.")
                elif len(results) == 1:
                    st.session_state.selected_player_id = results[0].get('id')
                else:
                    st.session_state.search_results = results

    if st.session_state.search_results:
        st.subheader("Multiple players found. Please choose one:")
        player_options = {
            f"{p.get('fullName', 'N/A')} ({p.get('primaryPosition', {}).get('abbreviation', 'N/A')}, {p.get('currentTeam', {}).get('name', 'N/A')})": p.get('id')
            for p in st.session_state.search_results
        }
        selected_option = st.radio("Select a player:", options=list(player_options.keys()), key="player_choice")
        if selected_option:
            st.session_state.selected_player_id = player_options[selected_option]
            st.session_state.search_results = None
            st.experimental_rerun()
    elif st.session_state.selected_player_id:
        display_player_stats(api, st.session_state.selected_player_id)

if __name__ == "__main__":
    main()
