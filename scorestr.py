import requests
from datetime import datetime
from datetime import time
from post_note import post_note
from get_notes import get_notes
from similarity_check import deduplicate_articles
import pytz
from season_checker import seasons
import logging

logging.basicConfig(level=logging.INFO)

sports_nsecs = {
    "football/nfl": "PFFNFL",
    "basketball/mens-college-basketball": "NCAAMBB",
    "basketball/nba": "NBA",
    "baseball/mlb": "FOXMLB"
}

def fetch_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def time_converter(input_time_string):
    # Convert the input string to a datetime object
    given_datetime = datetime.strptime(input_time_string, "%Y-%m-%dT%H:%MZ")

    # Convert the datetime to Eastern Time
    eastern = pytz.timezone('US/Eastern')
    eastern_time = given_datetime.replace(tzinfo=pytz.utc).astimezone(eastern)

    # Extract just the time part in standard time format (12-hour with AM/PM)
    time_in_standard = eastern_time.strftime("%I:%M %p")

    return time_in_standard

def todays_slate(data, current_date):
    # String init
    todays_slate = f"{current_date} games:"

    for event in data['events']:
        competitions = event.get('competitions')
        name = event.get('name')
        for competition in competitions:
            time = time_converter(event.get('date'))
            broadcasts = competition['broadcasts']
            if broadcasts and 'name' in broadcasts[0]:
                broadcast_name = broadcasts[0].get('name')
                todays_slate += f"\n{name} at {time} on {broadcast_name}"
            else:
                todays_slate += f"\n{name} at {time}"
        
    return todays_slate

    

def main():
    in_season_sports = seasons()

    # Get the current date
    current_date = datetime.now().date().strftime("%Y-%m-%d")
    current_time = datetime.now().time()

    # Game slate initializers
    slate_time_end = time(1, 00)
    

    for sport in in_season_sports:
        api_url = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/scoreboard"
        prev_notes = get_notes(sports_nsecs[sport])
    
        data = fetch_data_from_api(api_url)
        if data:
            # Data initialization
            date = data['day'].get('date')


            if date == current_date and current_time < slate_time_end:
                logging.info(f"Fetching game slate...")
                slate_post = todays_slate(data, current_date)
                is_duplicate = deduplicate_articles(slate_post, prev_notes)
                if is_duplicate == False:
                    post_note(slate_post, sports_nsecs[sport])

            for event in data['events']:
                competitions = event.get('competitions')
                for competition in competitions:
                    status = competition['status']
                    status_name = status.get('type').get('name')
                    status_detail = status.get('type').get('detail')
                    competitors = competition.get('competitors')
                    if status_name == 'STATUS_HALFTIME':
                        halftime_note = (f"{event['name']} HALFTIME score: {competitors[0]['team']['name']} {competitors[0]['score']} - {competitors[1]['team']['name']} {competitors[1]['score']}")
                        is_duplicate = deduplicate_articles(halftime_note, prev_notes)
                        if is_duplicate == False:
                            post_note(fulltime_note, sports_nsecs[sport])
                        else:
                            logging.info("Duplicate article found. Not posting to Nostr.")
                    elif status_name == 'STATUS_FINAL':
                        fulltime_note = (f"{event['name']} FINAL score: {competitors[0]['team']['name']} {competitors[0]['score']} - {competitors[1]['team']['name']} {competitors[1]['score']}")
                        is_duplicate = deduplicate_articles(fulltime_note, prev_notes)
                        if is_duplicate == False:
                            post_note(fulltime_note, sports_nsecs[sport])
                        else:
                            logging.info("Duplicate article found. Not posting to Nostr.")
                    elif status_name == 'STATUS_IN_PROGRESS' and status.get('period') == 5:
                        fulltime_note = (f"{event['name']} {status_detail} score: {competitors[0]['team']['name']} {competitors[0]['score']} - {competitors[1]['team']['name']} {competitors[1]['score']}")
                        is_duplicate = deduplicate_articles(fulltime_note, prev_notes)
                        if is_duplicate == False:
                            post_note(fulltime_note, sports_nsecs[sport])
                        else:
                            logging.info("Duplicate article found. Not posting to Nostr.")
                    else:
                        print(f"Game status: {status_name}")
            
            for event in data['events']:
                print(event['name'])
        else:
            print("No data fetched from API.")

if __name__ == "__main__":
    main()
