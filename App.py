import requests

API_KEY = "YOUR_ACTUAL_API_KEY_HERE" # Use your real key
MLB_API_BASE = "https://api.sportsdata.io/v3/mlb/scores/json" # Verify this base URL

# Example: Try fetching standings for a specific year
season_year = 2023 # Or current_year if you prefer
endpoint = f"Standings/{season_year}" # Verify this endpoint from SportsData.io docs

url = f"{MLB_API_BASE}/{endpoint}?key={API_KEY}"

print(f"Attempting to call URL: {url}")

try:
    response = requests.get(url)
    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    data = response.json()
    print("API Call Successful! Here's a snippet of the data:")
    print(data[:2]) # Print the first two items if it's a list, or the whole dict
except requests.exceptions.RequestException as e:
    print(f"API Call Failed: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response status code: {e.response.status_code}")
        print(f"Response body: {e.response.text}")
