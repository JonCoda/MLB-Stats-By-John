import streamlit as st
from MLBDeepDive import find_team, find_players
from LiveScores import live_scores

# --- Page Configuration ---
st.set_page_config(
    page_title="MLB Stats Finder",
    page_icon="⚾",
    layout="centered",
)

st.title("⚾ MLB Stats Finder")
st.write("Search for information about your favorite MLB teams and players.")

# --- Search UI ---
search_type = st.radio(
    "What do you want to search for?",
    ('Team', 'Player'),
    horizontal=True
)

if search_type == 'Team':
    # --- Team Search ---
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
    # --- Player Search ---
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

