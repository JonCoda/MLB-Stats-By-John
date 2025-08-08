import streamlit as st

def render_team_standings(season):
    st.warning("Team standings would be shown here (API code removed).")

def render_player_stats(player_id, season):
    st.error(f"Player stats for ID {player_id} in {season} would be shown here (API code removed).")

def main():
    st.set_page_config(page_title="MLB Stats Viewer", layout="wide")
    st.title("⚾ MLB Stats Viewer")

    current_year = 2024  # Example: Set current year manually
    min_year = 2000
    years = list(range(current_year, min_year - 1, -1))
    season = st.selectbox("Choose MLB season year:", years, index=0)

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
                st.session_state.selected_player_id = player_input
            else:
                st.session_state.search_results = [player_input]  # Use the input as a mock result

    if st.session_state.get('search_results'):
        st.subheader("Select a player:")
        choice = st.radio("Choose:", st.session_state.search_results, key="player_choice")
        if choice:
            st.session_state.selected_player_id = choice
            st.session_state.search_results = None
            st.experimental_rerun()
    elif st.session_state.get('selected_player_id'):
        render_player_stats(st.session_state.selected_player_id, season=season)

if __name__ == "__main__":
    main()
