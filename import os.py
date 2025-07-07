import os
import requests
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# --- Configuration ---
API_KEY = os.getenv("123")

if not API_KEY:
    # The free test key '1' is used as a fallback.
    # It's recommended to set your own key in a .env file.
    print("Warning: API_KEY not found in .env file. Using fallback test key '123'.")
    API_KEY = '123'

API_BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

@app.route('/')
def index():
    """Renders the main dashboard page."""
    return render_template('index.html')

@app.route('/api/live/<league_id>')
def get_live_games(league_id):
    """Proxy endpoint to fetch live games from TheSportsDB."""
    url = f"{API_BASE_URL}/eventslive.php?l={league_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching live games: {e}")
        return jsonify({"error": "Failed to fetch data from TheSportsDB"}), 500

@app.route('/api/upcoming/<league_id>')
def get_upcoming_games(league_id):
    """Proxy endpoint to fetch upcoming games from TheSportsDB."""
    url = f"{API_BASE_URL}/eventsnextleague.php?id={league_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching upcoming games: {e}")
        return jsonify({"error": "Failed to fetch data from TheSportsDB"}), 500

if __name__ == '__main__':
    # Use debug=False in a production environment
    app.run(debug=True, host='0.0.0.0')