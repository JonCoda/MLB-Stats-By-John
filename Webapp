<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MLB Information Hub</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom styles for better aesthetics and mobile responsiveness */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f0f2f5;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
        }
        .container {
            background-color: #ffffff;
            border-radius: 1.5rem; /* Rounded corners */
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin: 1rem;
            width: 100%;
            max-width: 800px;
            box-sizing: border-box;
        }
        .tab-button {
            padding: 0.75rem 1.25rem;
            border-radius: 0.75rem;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            cursor: pointer;
            text-align: center;
            white-space: nowrap; /* Prevent wrapping on small screens */
            flex-grow: 1; /* Allow buttons to grow */
        }
        .tab-button.active {
            background-color: #1a73e8; /* Google Blue */
            color: white;
            box-shadow: 0 4px 8px rgba(26, 115, 232, 0.3);
        }
        .tab-button:not(.active):hover {
            background-color: #e0e0e0;
        }
        .section-content {
            display: none;
            padding-top: 1rem;
        }
        .section-content.active {
            display: block;
        }
        .score-item {
            background-color: #f9f9f9;
            border-radius: 0.75rem;
            padding: 0.75rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        .score-item strong {
            color: #1a73e8;
        }
        .score-item span {
            font-size: 0.9rem;
            color: #666;
        }
        .loading-spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-top: 4px solid #1a73e8;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        h2 {
            color: #1a73e8;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        h3 {
            color: #333;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }
        p, ul {
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        ul {
            list-style-type: disc;
            padding-left: 1.5rem;
        }
        li {
            margin-bottom: 0.5rem;
        }

        /* Responsive adjustments */
        @media (max-width: 640px) {
            .tab-buttons-container {
                flex-direction: column;
            }
            .tab-button {
                margin-bottom: 0.5rem;
            }
            .container {
                margin: 0.5rem;
                padding: 1rem;
            }
        }
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center">
    <div class="container bg-white rounded-3xl shadow-xl p-6 md:p-8 lg:p-10">
        <h1 class="text-4xl font-extrabold text-center text-blue-700 mb-6">⚾ MLB Info Hub</h1>

        <!-- Tab Navigation -->
        <div class="tab-buttons-container flex flex-wrap gap-2 mb-6 justify-center">
            <button class="tab-button active bg-blue-600 text-white" data-tab="live-scores">Live Scores</button>
            <button class="tab-button bg-gray-200 text-gray-700" data-tab="advanced-stats">Advanced Stats</button>
            <button class="tab-button bg-gray-200 text-gray-700" data-tab="general-info">General Info</button>
        </div>

        <!-- Live Scores Section -->
        <div id="live-scores" class="section-content active">
            <h2 class="text-2xl font-bold text-blue-700 mb-4">MLB Live Score Ticker</h2>
            <div id="scores-display" class="space-y-3">
                <div class="loading-spinner"></div>
                <p class="text-center text-gray-500 mt-4">Fetching live scores...</p>
            </div>
            <p class="text-sm text-gray-500 text-center mt-4">Scores refresh automatically every 30 seconds.</p>
        </div>

        <!-- Advanced Stats Section -->
        <div id="advanced-stats" class="section-content">
            <h2 class="text-2xl font-bold text-blue-700 mb-4">Understanding MLB Advanced Stats (Sabermetrics)</h2>
            <p class="text-gray-700">
                Advanced statistics, often called **Sabermetrics**, go beyond traditional stats like batting average or home runs to give a deeper understanding of a player's true value. They are widely used by teams and analysts now.
            </p>
            <p class="text-gray-700">
                Here are some key advanced stats and what they generally mean:
            </p>
            <ul class="list-disc list-inside text-gray-700">
                <li>
                    <h3>WAR (Wins Above Replacement)</h3>
                    <p>This is one of the most comprehensive stats. It estimates how many more wins a player contributes to their team compared to a "replacement-level" player (someone who could be easily acquired, like a minor leaguer). A higher WAR indicates a more valuable player. There are slightly different calculations (e.g., fWAR from FanGraphs, bWAR from Baseball-Reference).</p>
                </li>
                <li>
                    <h3>OPS+ (On-Base Plus Slugging Plus)</h3>
                    <p>This combines a player's On-Base Percentage (how often they get on base) and Slugging Percentage (how many bases they get per at-bat), adjusted for the league and ballpark. A score of 100 is league average; above 100 is better, below 100 is worse.</p>
                </li>
                <li>
                    <h3>wOBA (Weighted On-Base Average)</h3>
                    <p>This is similar to OPS+ but gives more weight to different types of hits (e.g., a double is worth more than a single) and walks, providing a more accurate measure of overall offensive contribution.</p>
                </li>
                <li>
                    <h3>FIP (Fielding Independent Pitching)</h3>
                    <p>For pitchers, this estimates what a pitcher's ERA (Earned Run Average) *should* have been, based only on events they control (strikeouts, walks, hit-by-pitches, and home runs). It removes the influence of defense.</p>
                </li>
                <li>
                    <h3>DRS (Defensive Runs Saved) / UZR (Ultimate Zone Rating) / OAA (Outs Above Average)</h3>
                    <p>These stats measure a player's defensive contribution, quantifying how many runs they saved or cost their team compared to an average fielder.</p>
                </li>
            </ul>
            <p class="text-gray-700">
                You can typically find these advanced statistics on dedicated baseball statistics websites like <a href="https://www.fangraphs.com/" target="_blank" class="text-blue-600 hover:underline">FanGraphs</a>, <a href="https://www.baseball-reference.com/" target="_blank" class="text-blue-600 hover:underline">Baseball-Reference.com</a>, or <a href="https://www.mlb.com/stats/statcast" target="_blank" class="text-blue-600 hover:underline">MLB.com's Statcast section</a>.
            </p>
        </div>

        <!-- General MLB Info Section -->
        <div id="general-info" class="section-content">
            <h2 class="text-2xl font-bold text-blue-700 mb-4">General MLB Information</h2>
            <p class="text-gray-700">
                Major League Baseball (MLB) is the highest level of professional baseball in the United States and Canada.
            </p>
            <ul class="list-disc list-inside text-gray-700">
                <li>
                    <h3>Teams</h3>
                    <p>It consists of 30 teams, divided equally into two leagues: the **American League (AL)** and the **National League (NL)**. Each league has three divisions (East, Central, West).</p>
                </li>
                <li>
                    <h3>Season</h3>
                    <p>The regular season runs from late March/early April to late September, with each team playing **162 games**.</p>
                </li>
                <li>
                    <h3>Postseason</h3>
                    <p>After the regular season, 12 teams (division winners and wild card teams) advance to a four-round postseason tournament in October, culminating in the **World Series**, a best-of-seven championship series between the AL and NL champions.</p>
                </li>
                <li>
                    <h3>History</h3>
                    <p>MLB is the oldest major professional sports league in the world, with its roots dating back to the 19th century. The first professional team, the Cincinnati Red Stockings, was established in 1869.</p>
                </li>
                <li>
                    <h3>Current Champions</h3>
                    <p>The Los Angeles Dodgers are the reigning World Series champions (they defeated the Yankees in the 2024 World Series).</p>
                </li>
                <li>
                    <h3>Most Championships</h3>
                    <p>The New York Yankees hold the record for the most World Series championships with 27.</p>
                </li>
            </ul>
        </div>
    </div>

    <script>
        // JavaScript for tab switching and live score fetching
        document.addEventListener('DOMContentLoaded', () => {
            const tabButtons = document.querySelectorAll('.tab-button');
            const sections = document.querySelectorAll('.section-content');
            const scoresDisplay = document.getElementById('scores-display');

            // Function to show a specific tab
            const showTab = (tabId) => {
                tabButtons.forEach(button => {
                    if (button.dataset.tab === tabId) {
                        button.classList.add('active', 'bg-blue-600', 'text-white');
                        button.classList.remove('bg-gray-200', 'text-gray-700');
                    } else {
                        button.classList.remove('active', 'bg-blue-600', 'text-white');
                        button.classList.add('bg-gray-200', 'text-gray-700');
                    }
                });

                sections.forEach(section => {
                    if (section.id === tabId) {
                        section.classList.add('active');
                    } else {
                        section.classList.remove('active');
                    }
                });
            };

            // Event listeners for tab buttons
            tabButtons.forEach(button => {
                button.addEventListener('click', () => {
                    showTab(button.dataset.tab);
                });
            });

            // Function to fetch and display live scores
            const getLiveScores = async () => {
                scoresDisplay.innerHTML = '<div class="loading-spinner"></div><p class="text-center text-gray-500 mt-4">Fetching live scores...</p>';
                const url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard";
                try {
                    const response = await fetch(url);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = await response.json();
                    const games = data.events || [];

                    if (games.length === 0) {
                        scoresDisplay.innerHTML = '<p class="text-center text-gray-600">No live games found at the moment.</p>';
                        return;
                    }

                    let scoresHtml = '';
                    games.forEach(game => {
                        const competition = game.competitions[0];
                        const status = competition.status.type.description;
                        const teams = competition.competitors;
                        const home = teams.find(team => team.homeAway === 'home');
                        const away = teams.find(team => team.homeAway === 'away');

                        scoresHtml += `
                            <div class="score-item">
                                <strong>${away.team.displayName} @ ${home.team.displayName}</strong>
                                <span>Score: ${away.score} - ${home.score}</span>
                                <span>Status: ${status}</span>
                            </div>
                        `;
                    });
                    scoresDisplay.innerHTML = scoresHtml;

                } catch (error) {
                    scoresDisplay.innerHTML = `<p class="text-center text-red-500">Error fetching scores: ${error.message}. Please try again later.</p>`;
                    console.error("Error fetching live scores:", error);
                }
            };

            // Initial fetch of scores
            getLiveScores();

            // Set up autorefresh for live scores every 30 seconds (30000 milliseconds)
            setInterval(getLiveScores, 30000);
        });
    </script>
</body>
</html>

