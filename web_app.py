from flask import Flask, jsonify
from flask_cors import CORS # Used to allow your HTML file to talk to this Python server
import requests
import time

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, allowing your HTML to fetch data

# --- Function to fetch live scores from ESPN API ---
def get_live_mlb_scores():
    """
    Fetches live MLB scores from ESPN API.
    Returns a list of game dictionaries or None on error.
    """
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    try:
        response = requests.get(url, timeout=7)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        games = data.get('events', [])
        scores = []
        for game in games:
            competition = game['competitions'][0]
            status = competition['status']['type']['detail']
            teams = competition['competitors']
            home = next(team for team in teams if team['homeAway'] == 'home')
            away = next(team for team in teams if team['homeAway'] == 'away')

            away_score = away.get('score', '0') if away.get('score') is not None else '0'
            home_score = home.get('score', '0') if home.get('score') is not None else '0'

            scores.append({
                "matchup": f"{away['team']['displayName']} @ {home['team']['displayName']}",
                "score": f"{away_score} - {home_score}",
                "status": status
            })
        return scores
    except requests.exceptions.RequestException as e:
        print(f"Error fetching live scores: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while processing scores: {e}")
        return None

# --- API Endpoints ---

@app.route('/api/scores', methods=['GET'])
def scores_api():
    """API endpoint to get live MLB scores."""
    scores = get_live_mlb_scores()
    if scores is None:
        return jsonify({"error": "Could not fetch live scores"}), 500
    return jsonify(scores)

@app.route('/api/advanced_stats', methods=['GET'])
def advanced_stats_api():
    """API endpoint to get advanced stats information."""
    # This is static content for explanation purposes
    advanced_stats_info = {
        "title": "Understanding MLB Advanced Stats (Sabermetrics)",
        "description": "Advanced statistics, often called Sabermetrics, go beyond traditional stats like batting average or home runs to give a deeper understanding of a player's true value. They are widely used by teams and analysts now.",
        "stats": [
            {
                "name": "WAR (Wins Above Replacement)",
                "explanation": "This is one of the most comprehensive stats. It estimates how many more wins a player contributes to their team compared to a 'replacement-level' player (someone who could be easily acquired, like a minor leaguer). A higher WAR indicates a more valuable player. There are slightly different calculations (e.g., fWAR from FanGraphs, bWAR from Baseball-Reference)."
            },
            {
                "name": "OPS+ (On-Base Plus Slugging Plus)",
                "explanation": "This combines a player's On-Base Percentage (how often they get on base) and Slugging Percentage (how many bases they get per at-bat), adjusted for the league and ballpark. A score of 100 is league average; above 100 is better, below 100 is worse."
            },
            {
                "name": "wOBA (Weighted On-Base Average)",
                "explanation": "This is similar to OPS+ but gives more weight to different types of hits (e.g., a double is worth more than a single) and walks, providing a more accurate measure of overall offensive contribution."
            },
            {
                "name": "FIP (Fielding Independent Pitching)",
                "explanation": "For pitchers, this estimates what a pitcher's ERA (Earned Run Average) *should* have been, based only on events they control (strikeouts, walks, hit-by-pitches, and home runs). It removes the influence of defense."
            },
            {
                "name": "DRS (Defensive Runs Saved) / UZR (Ultimate Zone Rating) / OAA (Outs Above Average)",
                "explanation": "These stats measure a player's defensive contribution, quantifying how many runs they saved or cost their team compared to an average fielder."
            }
        ],
        "resources": [
            {"name": "FanGraphs", "url": "https://www.fangraphs.com/"},
            {"name": "Baseball-Reference.com", "url": "https://www.baseball-reference.com/"},
            {"name": "MLB.com's Statcast section", "url": "https://www.mlb.com/stats/statcast"}
        ]
    }
    return jsonify(advanced_stats_info)

@app.route('/api/general_info', methods=['GET'])
def general_info_api():
    """API endpoint to get general MLB information."""
    # This is static content for explanation purposes
    general_info = {
        "title": "General MLB Information",
        "sections": [
            {
                "name": "Teams",
                "content": "It consists of 30 teams, divided equally into two leagues: the **American League (AL)** and the **National League (NL)**. Each league has three divisions (East, Central, West)."
            },
            {
                "name": "Season",
                "content": "The regular season runs from late March/early April to late September, with each team playing **162 games**."
            },
            {
                "name": "Postseason",
                "content": "After the regular season, 12 teams (division winners and wild card teams) advance to a four-round postseason tournament in October, culminating in the **World Series**, a best-of-seven championship series between the AL and NL champions."
            },
            {
                "name": "History",
                "content": "MLB is the oldest major professional sports league in the world, with its roots dating back to the 19th century. The first professional team, the Cincinnati Red Stockings, was established in 1869."
            },
            {
                "name": "Current Champions",
                "content": "The Los Angeles Dodgers are the reigning World Series champions (they defeated the Yankees in the 2024 World Series)."
            },
            {
                "name": "Most Championships",
                "content": "The New York Yankees hold the record for the most World Series championships with 27."
            }
        ]
    }
    return jsonify(general_info)

if __name__ == '__main__':
    # This runs the Flask server on your computer, usually at http://127.0.0.1:5000/
    app.run(debug=True) # debug=True allows for automatic reloading on code changes

