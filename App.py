# app.py
from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# Enable CORS for your frontend.
# If your frontend is served from 'http://localhost:8000' (or similar), specify it here.
# For development, '*' allows all origins, but be more restrictive in production.
CORS(app)

# Base URL for the MLB Stats API
MLB_STATS_API_BASE_URL = "https://statsapi.mlb.com/api/v1"

@app.route('/api/mlb/standings', methods=['GET'])
def get_mlb_standings():
    """
    Fetches MLB standings data from statsapi.mlb.com and formats it.
    """
    try:
        # Fetch standings for both AL (103) and NL (104) for the current season
        # Adjust 'season' as needed (e.g., '2024')
        response = requests.get(f"{MLB_STATS_API_BASE_URL}/standings?leagueId=103,104&season=2024&date=09/30/2024")
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        formatted_standings = {
            "American League": {
                "East": [], "Central": [], "West": []
            },
            "National League": {
                "East": [], "Central": [], "West": []
            }
        }

        # Parse the complex MLB Stats API response structure
        if 'records' in data:
            for league_record in data['records']:
                # Determine league name (e.g., "American League")
                league_name = league_record['league']['name']
                if league_name not in formatted_standings:
                    continue # Skip if not AL or NL for now

                for division_record in league_record['division']['teams']:
                    division_name = division_record['division']['name']
                    # Adjust division names to match the expected keys
                    if 'East' in division_name:
                        key_division = "East"
                    elif 'Central' in division_name:
                        key_division = "Central"
                    elif 'West' in division_name:
                        key_division = "West"
                    else:
                        continue

                    for team_record in division_record['teamRecords']:
                        team_data = {
                            'team': team_record['team']['name'],
                            'wins': team_record['wins'],
                            'losses': team_record['losses'],
                            'gb': team_record['gamesBack'],
                            'pct': team_record['winningPercentage'],
                            'streak': team_record['streak']['streakCode'] if 'streak' in team_record else '-',
                        }
                        formatted_standings[league_name][key_division].append(team_data)

        # Sort teams within each division by wins (descending)
        for league in formatted_standings:
            for division in formatted_standings[league]:
                formatted_standings[league][division].sort(key=lambda x: x['wins'], reverse=True)


        return jsonify(formatted_standings)

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching standings from MLB API: {e}")
        return jsonify({"error": "Could not fetch standings data"}), 500
    except KeyError as e:
        app.logger.error(f"Error parsing MLB API response for standings: Missing key {e}")
        return jsonify({"error": "Failed to parse standings data structure"}), 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected server error occurred"}), 500


@app.route('/api/mlb/players', methods=['GET'])
def get_mlb_players():
    """
    Fetches a list of active players and some basic stats from statsapi.mlb.com.
    Note: Getting comprehensive "advanced stats" for ALL players in one go is complex
    with this API. This fetches recent hitting/pitching stats.
    """
    try:
        # Fetch data for all active players in the 2024 season
        # This API response can be large. In a real app, you might filter this.
        # For simplicity, we'll fetch general hitting/pitching stats.
        # This endpoint gets common season stats. For specific "advanced" stats (like WAR, OPS+),
        # statsapi.mlb.com might require different stat types or calculations.
        # We'll use a broad endpoint for demonstration.
        
        # Example to get a list of active players
        # The /rosters endpoint gives players by team. More direct: a `people` endpoint.
        # A simpler way to get active players for general stats:
        
        # Fetch recent hitting stats for the season (e.g., 2024)
        hitting_response = requests.get(f"{MLB_STATS_API_BASE_URL}/stats?stats=season&group=hitting&season=2024")
        hitting_response.raise_for_status()
        hitting_data = hitting_response.json()
        
        # Fetch recent pitching stats for the season
        pitching_response = requests.get(f"{MLB_STATS_API_BASE_URL}/stats?stats=season&group=pitching&season=2024")
        pitching_response.raise_for_status()
        pitching_data = pitching_response.json()

        all_players_stats = []

        # Process hitting stats
        if 'stats' in hitting_data and len(hitting_data['stats']) > 0:
            for stat_group in hitting_data['stats'][0]['splits']:
                player_id = stat_group['player']['id']
                player_name = stat_group['player']['fullName']
                team_name = stat_group['team']['name'] if 'team' in stat_group else 'N/A'
                
                # Extract some common hitting stats
                stats = stat_group['stat']
                all_players_stats.append({
                    'player': player_name,
                    'team': team_name,
                    'stat': 'Games Played', 'value': stats.get('gamesPlayed', '-') , 'category': 'Batting'
                })
                 # Add more specific stats if available and relevant
                if 'avg' in stats: all_players_stats.append({'player': player_name, 'team': team_name, 'stat': 'AVG', 'value': stats['avg'], 'category': 'Batting'})
                if 'homeRuns' in stats: all_players_stats.append({'player': player_name, 'team': team_name, 'stat': 'HR', 'value': stats['homeRuns'], 'category': 'Batting'})
                if 'ops' in stats: all_players_stats.append({'player': player_name, 'team': team_name, 'stat': 'OPS', 'value': stats['ops'], 'category': 'Batting'})


        # Process pitching stats
        if 'stats' in pitching_data and len(pitching_data['stats']) > 0:
            for stat_group in pitching_data['stats'][0]['splits']:
                player_id = stat_group['player']['id']
                player_name = stat_group['player']['fullName']
                team_name = stat_group['team']['name'] if 'team' in stat_group else 'N/A'

                # Extract some common pitching stats
                stats = stat_group['stat']
                all_players_stats.append({
                    'player': player_name,
                    'team': team_name,
                    'stat': 'Games Pitched', 'value': stats.get('gamesPitched', '-') , 'category': 'Pitching'
                })
                # Add more specific stats if available and relevant
                if 'era' in stats: all_players_stats.append({'player': player_name, 'team': team_name, 'stat': 'ERA', 'value': stats['era'], 'category': 'Pitching'})
                if 'strikeouts' in stats: all_players_stats.append({'player': player_name, 'team': team_name, 'stat': 'K', 'value': stats['strikeouts'], 'category': 'Pitching'})
                if 'whip' in stats: all_players_stats.append({'player': player_name, 'team': team_name, 'stat': 'WHIP', 'value': stats['whip'], 'category': 'Pitching'})


        return jsonify(all_players_stats)

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching players from MLB API: {e}")
        return jsonify({"error": "Could not fetch players data"}), 500
    except KeyError as e:
        app.logger.error(f"Error parsing MLB API response for players: Missing key {e}")
        return jsonify({"error": "Failed to parse players data structure"}), 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected server error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000) # Runs on http://localhost:5000
