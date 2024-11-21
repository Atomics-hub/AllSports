# import random
# import requests
# from datetime import datetime, timedelta
# import pytz
# import subprocess
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.action_chains import ActionChains
# import time

# # Your timezone
# TIMEZONE = pytz.timezone('America/Los_Angeles')

# # List of your favorite teams with their ESPN IDs
# teams = {
#     'Manchester City': '382',
#     'New York Mets': '21',
#     'Dallas Cowboys': '6',
#     'Sacramento Kings': '23',
#     'New York Islanders': '12',
#     'Boise State Broncos': '68',
#     'Los Angeles Lakers': '13',
#     'Carolina Hurricanes': '7'
# }


# # def get_team_ids(sport, league):
# #     url = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/teams"
# #     response = requests.get(url)
# #     data = response.json()
# #     teams = data.get('sports', [])[0].get('leagues', [])[0].get('teams', [])
# #
# #     team_ids = {}
# #     for team in teams:
# #         team_name = team['team']['displayName']
# #         team_id = team['team']['id']
# #         team_ids[team_name] = team_id
# #         print(f"{team_name}: {team_id}")
# #
# #     return team_ids
# #
# # # Get team IDs for each sport and league
# #
# # # Soccer (English Premier League)
# # soccer_team_ids = get_team_ids("soccer", "eng.1")
# # print("Manchester City ID:", soccer_team_ids.get("Manchester City"))
# #
# # # MLB Baseball
# # mlb_team_ids = get_team_ids("baseball", "mlb")
# # print("New York Mets ID:", mlb_team_ids.get("New York Mets"))
# #
# # # NFL Football
# # nfl_team_ids = get_team_ids("football", "nfl")
# # print("Dallas Cowboys ID:", nfl_team_ids.get("Dallas Cowboys"))
# #
# # # Use "football/college-football" for NCAA College Football
# # college_football_team_ids = get_team_ids("football", "college-football")
# # print("Boise State Broncos ID:", college_football_team_ids.get("Boise State Broncos"))
# #
# # # NBA Basketball
# # nba_team_ids = get_team_ids("basketball", "nba")
# # print("Sacramento Kings ID:", nba_team_ids.get("Sacramento Kings"))
# #
# # # NHL Hockey
# # nhl_team_ids = get_team_ids("hockey", "nhl")
# # print("New York Islanders ID:", nhl_team_ids.get("New York Islanders"))


# def get_sport(team_name):
#     if team_name in ['Manchester City']:
#         return 'soccer/eng.1'
#     elif team_name in ['New York Mets']:
#         return 'baseball/mlb'
#     elif team_name in ['Dallas Cowboys']:
#         return 'football/nfl'
#     elif team_name in ['Boise State Broncos']:
#         return 'football/college-football'
#     elif team_name in ['Sacramento Kings', 'Los Angeles Lakers']:
#         return 'basketball/nba'
#     elif team_name in ['New York Islanders', 'Carolina Hurricanes']:
#         return 'hockey/nhl'


# def get_team_schedule(team_name, team_id):
#     url = f"https://site.api.espn.com/apis/site/v2/sports/{get_sport(team_name)}/teams/{team_id}/schedule"
#     print(f"Fetching schedule for {team_name} from {url}")

#     response = requests.get(url)
#     data = response.json()
#     games = data.get('events', [])

#     # Filter for games that are today or later
#     upcoming_games = []
#     for game in games:
#         game_time_str = game['date']
#         game_time = datetime.strptime(game_time_str, "%Y-%m-%dT%H:%MZ").replace(tzinfo=pytz.utc).astimezone(TIMEZONE)
#         print(f"Found game: {team_name} at {game_time} (local time)")

#         if game_time >= datetime.now(TIMEZONE) - timedelta(hours=3):  # Include games from the last 3 hours
#             upcoming_games.append(game)

#     print(f"Upcoming games for {team_name}: {[game['date'] for game in upcoming_games]}")
#     return upcoming_games


# def is_game_starting_soon(game):
#     game_time_str = game['date']
#     game_time = datetime.strptime(game_time_str, "%Y-%m-%dT%H:%MZ").replace(tzinfo=pytz.utc).astimezone(TIMEZONE)
#     time_to_game = game_time - datetime.now(TIMEZONE)
#     print(
#         f"Checking if game is starting soon. Game time (local): {game_time}, Time now: {datetime.now(TIMEZONE)}, Time to game: {time_to_game}")
#     return timedelta(minutes=0) < time_to_game <= timedelta(minutes=15)


# def turn_on_tv():
#     print("Turning on TV via cec-client")
#     subprocess.run('echo "on 0" | cec-client -s -d 1', shell=True)
#     # Switch to HDMI 3
#     subprocess.run('echo "tx 4F:82:30:00" | cec-client -s -d 1', shell=True)


# def open_stream(url, game):
#     print(f"Opening stream at URL: {url}")
#     chrome_options = Options()

#     # Memory-saving options for Raspberry Pi
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
#     chrome_options.add_argument("--disable-software-rasterizer")  # Disable software rasterization
#     chrome_options.add_argument("--disable-extensions")  # Disable extensions to save memory
#     chrome_options.add_argument("--disable-sync")  # Disable sync
#     chrome_options.add_argument("--disable-translate")  # Disable translation
#     chrome_options.add_argument("--disable-web-security")  # Disable web security for streaming
#     chrome_options.add_argument("--single-process")  # Run in single process mode
#     chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors
#     chrome_options.add_argument("--disable-features=TranslateUI")
#     chrome_options.add_argument("--disable-features=site-per-process")  # Disable site isolation
#     chrome_options.add_argument("--disable-breakpad")  # Disable crash reporting
#     chrome_options.add_argument("--disable-features=AudioServiceOutOfProcess")
#     chrome_options.add_argument("--disable-features=IsolateOrigins")
#     chrome_options.add_argument("--start-maximized")

#     # Set reasonable memory limits
#     chrome_options.add_argument("--js-flags=--max-old-space-size=128")  # Limit JS memory
#     chrome_options.add_argument("--memory-pressure-off")

#     # Use low-end device optimizations
#     chrome_options.add_argument("--enable-low-end-device-mode")
#     chrome_options.add_argument("--enable-low-res-tiling")

#     # Set a lower resolution to reduce memory usage
#     chrome_options.add_argument("--window-size=1280,720")

#     try:
#         driver = webdriver.Chrome(options=chrome_options)
#         driver.set_page_load_timeout(30)  # Set page load timeout

#         driver.get(url)
#         time.sleep(5)  # Reduced wait time

#         # Simplified video handling
#         try:
#             video_element = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.TAG_NAME, "video"))
#             )

#             # Simple fullscreen request
#             driver.execute_script("""
#                 const video = document.querySelector('video');
#                 if (video) {
#                     video.requestFullscreen().catch(console.error);
#                 }
#             """)

#             # Simplified monitoring loop
#             while True:
#                 time.sleep(30)
#                 if not is_game_in_progress(game):
#                     print("Game has ended. Closing the stream.")
#                     driver.quit()
#                     break

#         except Exception as e:
#             print(f"Video handling error: {e}")
#             driver.quit()

#     except Exception as e:
#         print(f"Browser error: {e}")
#         try:
#             driver.quit()
#         except:
#             pass


# def main():
#     checked_games = set()
#     while True:
#         for team_name, team_id in teams.items():
#             schedule = get_team_schedule(team_name, team_id)
#             for event in schedule:
#                 event_id = event['id']
#                 if event_id in checked_games:
#                     continue
#                 if is_game_starting_soon(event) or is_game_in_progress(event):
#                     checked_games.add(event_id)
#                     print(f"Game for {team_name} is starting or in progress!")
#                     turn_on_tv()
#                     sport = get_sport_simple(team_name)
#                     stream_url = get_stream_url(team_name, sport, event)

#                     # Start the stream in a separate thread to prevent blocking
#                     import threading
#                     stream_thread = threading.Thread(target=open_stream, args=(stream_url, event))
#                     stream_thread.daemon = True
#                     stream_thread.start()

#         time.sleep(60)  # Wait 1 minute before checking again


# def get_sport_simple(team_name):
#     if team_name == 'Manchester City':
#         return 'soccer'
#     elif team_name == 'New York Mets':
#         return 'mlb'
#     elif team_name == 'Dallas Cowboys':
#         return 'nfl'
#     elif team_name == 'Boise State Broncos':
#         return 'cfb'
#     elif team_name == 'Sacramento Kings' or team_name == 'Los Angeles Lakers':
#         return 'nba'
#     elif team_name == 'New York Islanders' or team_name == 'Carolina Hurricanes':
#         return 'nhl'


# def get_stream_url(team_name, sport, event):
#     # Extract opponent's name for constructing URL
#     opponent = event['competitions'][0]['competitors']
#     opponent_name = None
#     for team in opponent:
#         if team['team']['displayName'] != team_name:
#             opponent_name = team['team']['displayName']
#             break
#     if not opponent_name:
#         opponent_name = "unknown"

#     print(f"Game detected: {team_name} vs {opponent_name}")

#     # Determine the URL pattern based on the sport
#     if sport == 'nhl':  # Hockey
#         event_slug_1 = f"{team_name.lower().replace(' ', '-')}-{opponent_name.lower().replace(' ', '-')}"
#         event_slug_2 = f"{opponent_name.lower().replace(' ', '-')}-{team_name.lower().replace(' ', '-')}"
#         url_1 = f"https://www.streameast.co/{sport}/{event_slug_1}/"
#         url_2 = f"https://www.streameast.co/{sport}/{event_slug_2}/"

#     elif sport == 'soccer':  # Soccer
#         event_slug_1 = f"{team_name.lower().replace(' ', '-')}-vs-{opponent_name.lower().replace(' ', '-')}"
#         event_slug_2 = f"{opponent_name.lower().replace(' ', '-')}-vs-{team_name.lower().replace(' ', '-')}"
#         url_1 = f"https://www.streameast.co/{sport}/{event_slug_1}/"
#         url_2 = f"https://www.streameast.co/{sport}/{event_slug_2}/"

#     elif sport == 'nba':  # NBA
#         random_number = random.randint(0, 9)
#         event_slug_1 = f"{team_name.lower().replace(' ', '-')}-{opponent_name.lower().replace(' ', '-')}-{random_number}-live-stream"
#         event_slug_2 = f"{opponent_name.lower().replace(' ', '-')}-{team_name.lower().replace(' ', '-')}-{random_number}-live-stream"
#         url_1 = f"https://www.streameast.co/{sport}/{event_slug_1}/"
#         url_2 = f"https://www.streameast.co/{sport}/{event_slug_2}/"

#     elif sport == 'nfl':  # NBA
#         random_number = random.randint(0, 9)
#         event_slug_1 = f"{team_name.lower().replace(' ', '-')}-{opponent_name.lower().replace(' ', '-')}-{random_number}-live-stream"
#         event_slug_2 = f"{opponent_name.lower().replace(' ', '-')}-{team_name.lower().replace(' ', '-')}-{random_number}-live-stream"
#         url_1 = f"https://www.streameast.co/{sport}/{event_slug_1}/"
#         url_2 = f"https://www.streameast.co/{sport}/{event_slug_2}/"

#     elif sport == 'ncaaf':  # College Football
#         event_slug_1 = f"{team_name.lower().replace(' ', '-')}-{opponent_name.lower().replace(' ', '-')}"
#         event_slug_2 = f"{opponent_name.lower().replace(' ', '-')}-{team_name.lower().replace(' ', '-')}"
#         url_1 = f"https://www.streameast.co/{sport}/{event_slug_1}/"
#         url_2 = f"https://www.streameast.co/{sport}/{event_slug_2}/"

#     else:
#         print(f"Unknown sport: {sport}")
#         return None

#     # Try each constructed URL for validity
#     print(f"Trying URL 1: {url_1}")
#     if check_url_with_selenium(url_1, team_name, opponent_name):
#         print(f"Using URL 1: {url_1}")
#         return url_1

#     if url_2:  # Check second URL if applicable
#         print(f"Trying URL 2: {url_2}")
#         if check_url_with_selenium(url_2, team_name, opponent_name):
#             print(f"Using URL 2: {url_2}")
#             return url_2

#     if sport == 'nfl':
#         for i in range(10):
#             variant_url = f"{url_1}-{i}/2"  # Appends "-i" after `url_1`
#             print(f"Trying NFL URL variant: {variant_url}")
#             if check_url_with_selenium(variant_url, team_name, opponent_name):
#                 print(f"Using NFL URL variant: {variant_url}")
#                 return variant_url
#         for i in range(10):
#             variant_url = f"{url_2}-{i}/2"  # Appends "-i" after `url_2`
#             print(f"Trying NBA URL variant: {variant_url}")
#             if check_url_with_selenium(variant_url, team_name, opponent_name):
#                 print(f"Using NFL URL variant: {variant_url}")
#                 return variant_url

#     # For NBA, try appending -0 to -9 if the first URL failed
#     if sport == 'nba':
#         for i in range(10):
#             variant_url = f"{url_1[:-15]}-{i}-live-stream/2"
#             print(f"Trying NBA URL variant: {variant_url}")
#             if check_url_with_selenium(variant_url, team_name, opponent_name):
#                 print(f"Using NBA URL variant: {variant_url}")
#                 return variant_url
#         for i in range(10):
#             variant_url = f"{url_2[:-15]}-{i}-live-stream/2"
#             print(f"Trying NBA URL variant: {variant_url}")
#             if check_url_with_selenium(variant_url, team_name, opponent_name):
#                 print(f"Using NBA URL variant: {variant_url}")
#                 return variant_url

#     if sport == 'nhl':
#         for i in range(10):
#             variant_url = f"{url_1[:-1]}-{i}/"
#             print(f"Trying NHL URL variant: {variant_url}")
#             if check_url_with_selenium(variant_url, team_name, opponent_name):
#                 print(f"Using NHL URL variant: {variant_url}")
#                 return variant_url
#         for i in range(10):
#             variant_url = f"{url_2[:-1]}-{i}/"
#             print(f"Trying NHL URL variant: {variant_url}")
#             if check_url_with_selenium(variant_url, team_name, opponent_name):
#                 print(f"Using NHL URL variant: {variant_url}")
#                 return variant_url

#     # Fallback to the general sport page if all specific URLs fail
#     fallback_url = f"https://www.streameast.co/watch-{sport}-streams/"
#     print(f"No specific game URL found. Using fallback URL: {fallback_url}")
#     return fallback_url


# def check_url_with_selenium(url, team_name, opponent_name):
#     chrome_options = Options()

#     # Minimal options for URL checking
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument("--disable-software-rasterizer")
#     chrome_options.add_argument("--window-size=800,600")  # Smaller window size for checking
#     chrome_options.add_argument("--disable-javascript")  # Disable JS for initial check
#     chrome_options.add_argument("--single-process")

#     driver = webdriver.Chrome(options=chrome_options)
#     driver.set_page_load_timeout(15)  # Shorter timeout for checking

#     try:
#         driver.get(url)
#         time.sleep(3)  # Reduced wait time

#         # Simplified check for stream availability
#         page_text = driver.page_source.lower()
#         team_variations = [
#             team_name.lower(),
#             opponent_name.lower(),
#             team_name.lower().replace(' ', '-'),
#             opponent_name.lower().replace(' ', '-')
#         ]

#         has_video = any(x in page_text for x in ['video', 'player', 'stream'])
#         has_team = any(variation in page_text for variation in team_variations)

#         return has_video and has_team

#     except Exception as e:
#         print(f"Error checking URL {url}: {e}")
#         return False
#     finally:
#         driver.quit()


# # def check_url_with_selenium(url, team_name, opponent_name):
# #     chrome_options = Options()
# #     chrome_options.add_argument("--headless")
# #     chrome_options.add_argument("--no-sandbox")
# #     chrome_options.add_argument("--disable-dev-shm-usage")
# #     chrome_options.add_argument(
# #         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# #     )
# #
# #     driver = webdriver.Chrome(options=chrome_options)
# #     try:
# #         driver.get(url)
# #         time.sleep(10)  # Wait for dynamic content
# #
# #         def check_player_elements():
# #             # Essential player elements that must be present
# #             player_selectors = [
# #                 ".player-poster.clickable",
# #                 ".play-wrapper",
# #                 "svg.poster-icon",
# #                 ".plyr__control--overlaid",
# #                 ".vjs-big-play-button",
# #                 "video",
# #                 ".video-js",
# #                 ".plyr"
# #             ]
# #
# #             for selector in player_selectors:
# #                 try:
# #                     element = WebDriverWait(driver, 3).until(
# #                         EC.presence_of_element_located((By.CSS_SELECTOR, selector))
# #                     )
# #                     print(f"Found player element: {selector}")
# #                     return True
# #                 except TimeoutException:
# #                     continue
# #             return False
# #
# #         # Check main page first
# #         player_found = check_player_elements()
# #
# #         # If no player found, check iframes
# #         if not player_found:
# #             iframes = driver.find_elements(By.TAG_NAME, "iframe")
# #             for iframe in iframes:
# #                 try:
# #                     iframe_src = iframe.get_attribute('src')
# #                     if not iframe_src or any(x in iframe_src.lower() for x in ['chat', 'advertisement', 'ads']):
# #                         continue
# #
# #                     print(f"Checking iframe: {iframe_src}")
# #
# #                     # Verify iframe size
# #                     size = iframe.size
# #                     if size['width'] < 200 or size['height'] < 150:
# #                         continue
# #
# #                     driver.switch_to.frame(iframe)
# #                     player_found = check_player_elements()
# #                     driver.switch_to.default_content()
# #
# #                     if player_found:
# #                         break
# #
# #                 except Exception as e:
# #                     print(f"Error checking iframe: {e}")
# #                     driver.switch_to.default_content()
# #                     continue
# #
# #         # Check for team names
# #         page_text = driver.page_source.lower()
# #         team_variations = [
# #             team_name.lower(),
# #             team_name.lower().replace(' ', ''),
# #             team_name.lower().replace(' ', '-'),
# #             opponent_name.lower(),
# #             opponent_name.lower().replace(' ', ''),
# #             opponent_name.lower().replace(' ', '-')
# #         ]
# #         team_found = any(variation in page_text for variation in team_variations)
# #
# #         if player_found and team_found:
# #             print(f"Valid stream found at {url} - Player and team names confirmed")
# #             return True
# #         else:
# #             print(f"Invalid stream at {url} - Player found: {player_found}, Team found: {team_found}")
# #             return False
# #
# #     except Exception as e:
# #         print(f"Error checking URL {url}: {e}")
# #         return False
# #     finally:
# #         driver.quit()


# def is_game_in_progress(game):
#     game_time_str = game['date']
#     game_time = datetime.strptime(game_time_str, "%Y-%m-%dT%H:%MZ").replace(tzinfo=pytz.utc).astimezone(TIMEZONE)
#     time_since_game = datetime.now(TIMEZONE) - game_time
#     game_duration = timedelta(hours=3)  # Assuming average game duration

#     print(
#         f"Checking if game is in progress. Game time (local): {game_time}, Time now: {datetime.now(TIMEZONE)}, Time since game start: {time_since_game}")

#     return timedelta(minutes=0) <= time_since_game <= game_duration


# if __name__ == "__main__":
#     main()

from datetime import datetime, timedelta
import pytz
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import requests
import time
import json

# Your timezone
from selenium.webdriver.support.wait import WebDriverWait

TIMEZONE = pytz.timezone('America/Los_Angeles')

# List of your favorite teams with their ESPN IDs
teams = {
    'Manchester City': '382',
    'New York Mets': '21',
    'Dallas Cowboys': '6',
    'Sacramento Kings': '23',
    'New York Islanders': '12',
    'Boise State Broncos': '68',
}


def get_sport(team_name):
    if team_name in ['Manchester City']:
        return 'soccer/eng.1'
    elif team_name in ['New York Mets']:
        return 'baseball/mlb'
    elif team_name in ['Dallas Cowboys']:
        return 'football/nfl'
    elif team_name in ['Boise State Broncos']:
        return 'football/college-football'
    elif team_name in ['Sacramento Kings']:
        return 'basketball/nba'
    elif team_name in ['New York Islanders']:
        return 'hockey/nhl'


cache_data = {}
for team_name, team_id in teams.items():
    url = f"https://site.api.espn.com/apis/site/v2/sports/{get_sport(team_name)}/teams/{team_id}/schedule"
    print(f"Fetching schedule for {team_name} from {url}")

    response = requests.get(url)
    data = response.json()
    cache_data[team_name] = data.get('events', [])

# Save the data to a JSON file
with open("schedule_cache.json", "w") as file:
    json.dump(cache_data, file)

print("Schedule data saved to schedule_cache.json")


def load_cache():
    try:
        with open("schedule_cache.json", "r") as file:
            cache_data = json.load(file)
            print("Loaded schedule data from cache.")
            return cache_data
    except FileNotFoundError:
        print("Cache file not found. No schedule data available.")
        return {}


# Get the cached schedule data for a specific team
def get_team_schedule_from_cache(team_name):
    cache_data = load_cache()
    if team_name in cache_data:
        upcoming_games = []
        games = cache_data[team_name]

        # Filter for games that are today or later
        for game in games:
            game_time_str = game['date']
            game_time = datetime.strptime(game_time_str, "%Y-%m-%dT%H:%MZ")
            # Assuming the timezone and other handling, add or modify as needed
            if game_time >= datetime.now() - timedelta(hours=3):  # Include games from the last 3 hours
                upcoming_games.append(game)

        print(f"Upcoming games for {team_name}: {[game['date'] for game in upcoming_games]}")
        return upcoming_games
    else:
        print(f"No cached data for team {team_name}")
        return []


def get_sport_simple(team_name):
    if team_name == 'Manchester City':
        return 'soccer'
    elif team_name == 'New York Mets':
        return 'mlb'
    elif team_name == 'Dallas Cowboys':
        return 'nfl'
    elif team_name == 'Boise State Broncos':
        return 'ncaaf'
    elif team_name in ['Sacramento Kings']:
        return 'nba'
    elif team_name in ['New York Islanders']:
        return 'nhl'


def get_team_schedule(team_name, team_id):
    url = f"https://site.api.espn.com/apis/site/v2/sports/{get_sport(team_name)}/teams/{team_id}/schedule"
    print(f"Fetching schedule for {team_name} from {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for HTTP status codes 4xx/5xx
        data = response.json()
        games = data.get('events', [])

    except requests.RequestException as e:
        print(f"Error fetching schedule from API: {e}")
        # Load data from cache if API request fails
        cache_data = load_cache()
        games = cache_data.get(team_name, [])

    # Filter for games that are today or later
    upcoming_games = []
    for game in games:
        game_time_str = game['date']
        game_time = datetime.strptime(game_time_str, "%Y-%m-%dT%H:%MZ").replace(tzinfo=pytz.utc).astimezone(TIMEZONE)
        print(f"Found game: {team_name} at {game_time} (local time)")

        if game_time >= datetime.now(TIMEZONE) - timedelta(hours=3):  # Include games from the last 3 hours
            upcoming_games.append(game)

    print(f"Upcoming games for {team_name}: {[game['date'] for game in upcoming_games]}")
    return upcoming_games


def is_game_starting_soon(game):
    game_time_str = game['date']
    game_time = datetime.strptime(game_time_str, "%Y-%m-%dT%H:%MZ").replace(tzinfo=pytz.utc).astimezone(TIMEZONE)
    time_to_game = game_time - datetime.now(TIMEZONE)
    print(
        f"Checking if game is starting soon. Game time (local): {game_time}, Time now: {datetime.now(TIMEZONE)}, Time to game: {time_to_game}")
    return timedelta(minutes=0) < time_to_game <= timedelta(minutes=15)


def turn_on_tv():
    print("Turning on TV via cec-client")
    subprocess.run('echo "on 0" | cec-client -s -d 1', shell=True)
    # Switch to HDMI 3
    subprocess.run('echo "tx 4F:82:30:00" | cec-client -s -d 1', shell=True)


def get_stream_url(team_name, sport, event):
    # Extract opponent's name for constructing URL
    opponent = event['competitions'][0]['competitors']
    opponent_name = None
    for team in opponent:
        if team['team']['displayName'] != team_name:
            opponent_name = team['team']['displayName']
            break
    if not opponent_name:
        opponent_name = "unknown"

    print(f"Game detected: {team_name} vs {opponent_name}")

    # For NHL games, construct URLs accordingly
    if sport == 'nhl' or sport == 'mlb':
        # Create possible URL patterns
        team1 = team_name.lower().replace(' ', '-')
        team2 = opponent_name.lower().replace(' ', '-')

        base_url = 'http://dofusports.xyz/games/'

        urls = [
            f"{base_url}{team1}-at-{team2}-home/",
            f"{base_url}{team1}-at-{team2}-away/",
            f"{base_url}{team2}-at-{team1}-home/",
            f"{base_url}{team2}-at-{team1}-away/"
        ]

        return urls

    if sport == 'nba' or sport == 'nfl':
        # Create possible URL patterns
        team1 = team_name.lower().replace(' ', '-')
        team2 = opponent_name.lower().replace(' ', '-')

        base_url = 'http://dofusports.xyz/games/'

        urls = [
            # f"{base_url}{team1}-at-{team2}-main/",
            # f"{base_url}{team1}-at-{team2}-alt/",
            f"{base_url}{team2}-at-{team1}-main/",
            f"{base_url}{team2}-at-{team1}-alt/"
        ]

        return urls

    else:
        # Handle other sports if needed
        # For now, let's return None
        print(f"Stream URL generation not implemented for sport: {sport}")
        return None


def is_game_in_progress(game):
    game_time_str = game['date']
    game_time = datetime.strptime(game_time_str, "%Y-%m-%dT%H:%MZ").replace(tzinfo=pytz.utc).astimezone(TIMEZONE)
    time_since_game = datetime.now(TIMEZONE) - game_time
    game_duration = timedelta(hours=3)  # Assuming average game duration

    print(
        f"Checking if game is in progress. Game time (local): {game_time}, Time now: {datetime.now(TIMEZONE)}, Time since game start: {time_since_game}")

    return timedelta(minutes=0) <= time_since_game <= game_duration


def setup_ublock(chrome_options):
    """Download and add uBlock Origin to Chrome"""
    # uBlock Origin extension ID
    UBLOCK_ID = 'cjpalhdlnbpafiamejdnhcphjbkeiagm'

    # Create extensions directory if it doesn't exist
    extensions_dir = os.path.join(os.getcwd(), 'chrome_extensions')
    os.makedirs(extensions_dir, exist_ok=True)

    # Download uBlock Origin
    ublock_download_url = f'https://clients2.google.com/service/update2/crx?response=redirect&os=win&arch=x64&os_arch=x86_64&nacl_arch=x86-64&prod=chromium&prodchannel=unknown&prodversion=88.0.4324.150&lang=en-US&acceptformat=crx2,crx3&x=id%3D{UBLOCK_ID}%26installsource%3Dondemand%26uc'
    ublock_path = os.path.join(extensions_dir, 'ublock_origin.crx')

    if not os.path.exists(ublock_path):
        response = requests.get(ublock_download_url)
        with open(ublock_path, 'wb') as f:
            f.write(response.content)

    chrome_options.add_extension(ublock_path)
    return chrome_options


def open_stream(urls, game):
    print(f"Opening stream at URLs: {urls}")

    for url in urls:
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")

        # Add additional options to handle ads and scripts
        chrome_options.add_argument("--disable-javascript-harmony-shipping")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-breakpad")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-default-apps")

        # Add uBlock Origin
        try:
            chrome_options = setup_ublock(chrome_options)
        except Exception as e:
            print(f"Failed to setup uBlock: {e}")

        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            driver.set_script_timeout(30)  # Increase script timeout

            print(f"Trying URL: {url}")
            driver.get(url)

            # Wait for uBlock to initialize and block initial ads
            time.sleep(10)

            try:
                wait = WebDriverWait(driver, 15)

                # Handle any remaining overlay
                try:
                    overlay = driver.find_element(By.ID, "dontfoid")
                    driver.execute_script("arguments[0].remove();", overlay)
                    print("Removed blocking overlay")
                except:
                    print("No blocking overlay found")

                # Find and switch to iframe
                print("Looking for iframe...")
                iframe = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[allow*='encrypted-media']"))
                )
                print(f"Found iframe with src: {iframe.get_attribute('src')}")

                # Ensure iframe is visible
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", iframe)
                time.sleep(2)

                print("Switching to iframe...")
                driver.switch_to.frame(iframe)
                time.sleep(2)

                print("Looking for player elements...")

                # Try multiple methods to start playback with shorter timeouts
                try:
                    # Method 1: Direct click on play wrapper
                    play_wrapper = wait.until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "play-wrapper"))
                    )
                    actions = ActionChains(driver)
                    actions.move_to_element(play_wrapper).click().perform()
                    print("Clicked play wrapper using Actions")
                except Exception as e:
                    print(f"Method 1 failed: {e}")
                    try:
                        # Method 2: JavaScript click with shorter timeout
                        driver.set_script_timeout(5)
                        driver.execute_script("document.querySelector('.play-wrapper').click();")
                        print("Clicked play wrapper using JavaScript")
                    except Exception as e:
                        print(f"Method 2 failed: {e}")

                # Look for video element
                print("Looking for video element...")
                video = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'video[data-html5-video]'))
                )
                print("Found video element")

                # Simplified playback script with shorter timeout
                print("Attempting playback...")
                driver.set_script_timeout(5)
                driver.execute_script("""
                    var video = arguments[0];
                    video.muted = true;
                    video.autoplay = true;
                    video.controls = true;
                    video.play();
                """, video)

                # Wait briefly for playback to start
                time.sleep(2)

                # Simple playback check
                is_playing = driver.execute_script("""
                    var video = arguments[0];
                    return !video.paused && video.currentTime > 0;
                """, video)

                if is_playing:
                    print("Video is playing successfully!")

                    # Try fullscreen
                    print("Attempting fullscreen...")
                    driver.execute_script("""
                        var video = arguments[0];
                        if (video.requestFullscreen) {
                            video.requestFullscreen();
                        } else if (video.webkitRequestFullscreen) {
                            video.webkitRequestFullscreen();
                        }
                    """, video)
                    # Try enhanced fullscreen methods
                    if try_fullscreen(driver, video):
                        print("Successfully entered fullscreen mode")
                    else:
                        print("Warning: Could not achieve fullscreen, but video is playing")

                    return driver
                else:
                    print("Video playback verification failed")
                    raise Exception("Could not verify video playback")

            except Exception as e:
                print(f"Error during video playback setup: {e}")
                try:
                    driver.switch_to.default_content()
                except:
                    pass
                print(f"Page source at time of error: {driver.page_source[:500]}...")
                driver.quit()
                continue

        except Exception as e:
            print(f"Browser error when trying URL {url}: {e}")
            if 'driver' in locals():
                driver.quit()
            continue

    print("Could not find a working stream.")
    return None


def try_fullscreen(driver, video):
    """Try multiple methods to achieve fullscreen, including double click"""
    print("Attempting fullscreen with multiple methods...")

    # Method 1: Double click on video (new primary method)
    try:
        print("Trying double click method...")
        actions = ActionChains(driver)
        actions.move_to_element(video)
        actions.double_click()
        actions.perform()
        time.sleep(1.5)  # Wait a bit longer for double click to register

        # Verify fullscreen
        is_fullscreen = driver.execute_script("""
            return !!(document.fullscreenElement || 
                     document.webkitFullscreenElement || 
                     document.mozFullScreenElement ||
                     document.msFullscreenElement);
        """)

        if is_fullscreen:
            print("Fullscreen achieved with double click!")
            return True
    except Exception as e:
        print(f"Double click method failed: {e}")

    # Method 2: JavaScript double click simulation
    try:
        print("Trying JavaScript double click simulation...")
        driver.execute_script("""
            var video = arguments[0];
            var clickEvent = new MouseEvent('dblclick', {
                'view': window,
                'bubbles': true,
                'cancelable': true
            });
            video.dispatchEvent(clickEvent);
        """, video)
        time.sleep(1.5)

        is_fullscreen = driver.execute_script("""
            return !!(document.fullscreenElement || 
                     document.webkitFullscreenElement || 
                     document.mozFullScreenElement ||
                     document.msFullscreenElement);
        """)

        if is_fullscreen:
            print("Fullscreen achieved with JavaScript double click!")
            return True
    except Exception as e:
        print(f"JavaScript double click method failed: {e}")

    # Fallback methods
    methods = [
        # Method 3: Try video element directly
        """
        var video = arguments[0];
        if (video.requestFullscreen) video.requestFullscreen();
        else if (video.mozRequestFullScreen) video.mozRequestFullScreen();
        else if (video.webkitRequestFullscreen) video.webkitRequestFullscreen();
        else if (video.msRequestFullscreen) video.msRequestFullscreen();
        """,

        # Method 4: Try container element
        """
        var container = document.querySelector('.container');
        if (container) {
            if (container.requestFullscreen) container.requestFullscreen();
            else if (container.mozRequestFullScreen) container.mozRequestFullScreen();
            else if (container.webkitRequestFullscreen) container.webkitRequestFullscreen();
            else if (container.msRequestFullscreen) container.msRequestFullscreen();
        }
        """
    ]

    for i, method in enumerate(methods, 3):
        try:
            print(f"Trying fullscreen method {i}...")
            driver.execute_script(method, video)
            time.sleep(1)

            is_fullscreen = driver.execute_script("""
                return !!(document.fullscreenElement || 
                         document.webkitFullscreenElement || 
                         document.mozFullScreenElement ||
                         document.msFullscreenElement);
            """)

            if is_fullscreen:
                print(f"Fullscreen achieved with method {i}")
                return True

        except Exception as e:
            print(f"Fullscreen method {i} failed: {e}")
            continue

    return False


def main():
    checked_games = set()
    active_stream = None  # Keep track of active stream
    active_game = None  # Keep track of active game

    while True:
        # If we have an active stream, check if the game is still in progress
        if active_stream and active_game:
            if is_game_in_progress(active_game):
                print("Game still in progress, continuing to stream...")
                time.sleep(60)
                continue
            else:
                print("Game has ended, closing stream...")
                active_stream.quit()
                active_stream = None
                active_game = None

        # Only check schedules if we're not streaming
        if not active_stream:
            for team_name, team_id in teams.items():
                schedule = get_team_schedule(team_name, team_id)
                for event in schedule:
                    event_id = event['id']
                    if event_id in checked_games:
                        continue
                    # Check if the game is starting soon or in progress
                    if is_game_starting_soon(event) or is_game_in_progress(event):
                        checked_games.add(event_id)
                        print(f"Game for {team_name} is starting or in progress!")
                        turn_on_tv()
                        sport = get_sport_simple(team_name)
                        stream_urls = get_stream_url(team_name, sport, event)

                        if stream_urls:
                            active_stream = open_stream(stream_urls, event)
                            if active_stream:
                                active_game = event
                                print("Stream started successfully")
                                break  # Exit the event loop
                        else:
                            print(f"No stream URL available for {team_name}")

                if active_stream:
                    break  # Exit the team loop if we found a stream

        time.sleep(60)  # Wait before next check


if __name__ == "__main__":
    main()
