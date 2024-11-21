import datetime
from web_extract import *
from unidecode import unidecode

date = str(datetime.datetime.now())[:10]

# json from mlb.com containing daily matchups and probable pitchers
daily_schedule_json = f'https://statsapi.mlb.com/api/v1/schedule?sportId=1&sportId=51&sportId=21&startDate={date}&endDate={date}&timeZone=America/New_York&hydrate=team(venue(timezone)),linescore(matchup,runners),xrefId,story,flags,statusFlags,venue(location),decisions,person,probablePitcher'

todays_schedule = get_json(daily_schedule_json)['dates'][0]['games'] # isolate schedule data within json

# create list that contains lists of game matchups and pitchers
def games_csv_format():
    all_game_info = []
    sides = ['away','home']
    for game in todays_schedule:
        time = game['gameDate'][11:16]
        for side in sides:
            try:
                pitcher_name = unidecode(game['teams'][side]['probablePitcher']['fullName']) # use unidecode to convert all characters to ASCII
                team = game['teams'][side]['team']['name']
            except:
                pitcher_name = 'TBD' # if pitcher not posted yet
                team = game['teams'][side]['team']['name']
                
            all_game_info.append([team,pitcher_name])
        all_game_info.append([])
    
    return all_game_info

# Code Execution
games = games_csv_format()
write_csv(games, 'games')