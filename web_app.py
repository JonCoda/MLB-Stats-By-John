pkg install python
pip install requests
termux-setup-storage
mlb_scores.py 
import requests # This library helps us get information from websites

def get_live_mlb_scores():
    """
    Fetches live MLB scores from a public ESPN API and returns them.
    This function will try to get the latest scores from the internet.
    """
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    print("Attempting to fetch live MLB scores...") # Let the user know what's happening

    try:
        # Try to get the data from the ESPN website.
        # We set a timeout so it doesn't wait forever if there's no internet.
        response = requests.get(url, timeout=10)

        # If the website sends back an error (like "page not found"), this will stop the program.
        response.raise_for_status()

        # Convert the website's response (which is in a special format called JSON)
        # into something Python can easily understand (like a dictionary).
        data = response.json()

        # The actual game information is usually in a list called 'events'.
        games = data.get('events', []) # If 'events' isn't there, it gives an empty list

        if not games:
            print("No live games found at the moment.")
            return

        print("\n--- Current MLB Live Scores ---")
        for game in games:
            # Each 'game' has details like teams, scores, and status.
            competition = game['competitions'][0] # Get the main competition details
            status = competition['status']['type']['detail'] # e.g., "Final", "In Progress"
            teams = competition['competitors'] # List of teams in the game

            # Find the home and away teams
            home_team = next(team for team in teams if team['homeAway'] == 'home')
            away_team = next(team for team in teams if team['homeAway'] == 'away')

            # Get their display names and scores. If score is missing, default to '0'.
            away_display_name = away_team['team']['displayName']
            home_display_name = home_team['team']['displayName']
            away_score = away_team.get('score', '0') if away_team.get('score') is not None else '0'
            home_score = home_team.get('score', '0') if home_team.get('score') is not None else '0'

            # Print the game information in a readable format
            print(f"{away_display_name} ({away_score}) vs {home_display_name} ({home_score}) - Status: {status}")
        print("-----------------------------\n")

    except requests.exceptions.RequestException as e:
        # This catches errors related to internet connection or the website itself
        print(f"Error fetching scores: Could not connect to the internet or the MLB data source. ({e})")
    except Exception as e:
        # This catches any other unexpected errors
        print(f"An unexpected error occurred: {e}")

# This line calls the function to get and print the scores when the script runs.
if __name__ == "__main__":
    get_live_mlb_scores()