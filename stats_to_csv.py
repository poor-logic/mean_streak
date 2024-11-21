import datetime
from web_extract import *
import pandas as pd
from unidecode import unidecode

# The year variable is used to update the json addresses from year to year
year = str(datetime.datetime.now())[:4]

# Addresses for JSON stat files
# Team Stats

# Bullpen Stats
bullpen_stats_json = f'https://bdfed.stitch.mlbinfra.com/bdfed/stats/team?&env=prod&sportId=1&gameType=R&group=pitching&order=asc&sortStat=earnedRunAverage&stats=season&season={year}&limit=30&offset=0&sitCodes=rp'

# Team batting stats
team_batting_json = f'https://bdfed.stitch.mlbinfra.com/bdfed/stats/team?&env=prod&sportId=1&gameType=R&group=hitting&order=desc&sortStat=battingAverage&stats=season&season={year}&limit=30&offset=0'


# Individual Stats
# Pitcher Stats
pitcher_json = f'https://bdfed.stitch.mlbinfra.com/bdfed/stats/player?&env=prod&season={year}&sportId=1&stats=season&group=pitching&gameType=R&limit=800&offset=0&sortStat=earnedRunAverage&order=desc&playerPool=ALL_CURRENT'

pitcher_career_json = 'https://bdfed.stitch.mlbinfra.com/bdfed/stats/player?&env=prod&sportId=1&stats=career&group=pitching&gameType=R&limit=800&offset=0&sortStat=earnedRunAverage&order=desc&playerPool=ALL_CURRENT'

# Hitter Stats
hitter_json = f'https://bdfed.stitch.mlbinfra.com/bdfed/stats/player?&env=prod&season={year}&sportId=1&stats=season&group=hitting&gameType=R&limit=800&offset=0&sortStat=onBasePlusSlugging&order=desc&playerPool=qualified'

              
# Format JSON into a clean workable version(works with pandas)
def data_clean_json(keys,data):
    cleaned_data = {}

    for item in data:
        name = item[keys[0]]
        cleaned_data[name] = {}
        for key in keys[1:]:
            cleaned_data[name][clean_labels[key]] = item[key]
            
    return cleaned_data

# Format JSON data into lists (prepping data for write_csv
def data_clean_csv(keys,data):
    cleaned_data = []
    headers = [clean_labels[x] for x in keys]
    cleaned_data.append(headers)
    for item in data:
        cleaned_row = []
        for key in keys:
            if 'Name' in key:
                cleaned_row.append(unidecode(item[key]))
            else:
                cleaned_row.append(item[key])
        cleaned_data.append(cleaned_row)
            
    return cleaned_data

   
# Function that enables the calling of variable names 
def var_name(obj):
    return [name for name in globals() if globals()[name] is obj][0]

# Function to read text file for JSON keys
def get_keys(stat_type):
    keys = []
    with open(f'.\\Data\\input\\{stat_type}.txt', 'r', newline='') as file:
        for line in file:
            keys.append(line.strip())
    return keys
    
# Function to read text file for clean labels
def get_labels():
    labels = {}
    with open('.\\Data\\input\\clean_labels.txt', 'r', newline='') as file:
        for line in file:
            seperate = line.split(',')
            labels[seperate[0]] = seperate[1].strip()
    return labels

clean_labels = get_labels()

# Individual stats and keys
pitcher_stats = get_json(pitcher_json)['stats']
pitcher_stat_keys = get_keys('pitcher_stat_keys')
pitcher_stat_data = data_clean_csv(pitcher_stat_keys,pitcher_stats)

#pitcher_career_stats = get_json(pitcher_career_json)['stats']
#pitcher_career_stat_keys = get_keys('pitcher_career_stat_keys')
#pitcher_career_stat_data = data_clean_csv(pitcher_career_stat_keys,pitcher_career_stats)

hitter_stats = get_json(hitter_json)['stats']
hitter_stat_keys = get_keys('hitter_stat_keys')
hitter_stat_data = data_clean_csv(hitter_stat_keys,hitter_stats)

# Team stats and keys
team_batting_stats = get_json(team_batting_json)['stats']
team_batting_stat_keys = get_keys('team_batting_stat_keys')
team_batting_stat_data = data_clean_csv(team_batting_stat_keys,team_batting_stats)

bullpen_stats = get_json(bullpen_stats_json)['stats']
bullpen_stat_keys = get_keys('bullpen_stat_keys')
bullpen_stat_data = data_clean_csv(bullpen_stat_keys,bullpen_stats)



# Write data to csv files
write_csv(pitcher_stat_data,'pitcher_stats') # Pitcher
#write_csv(pitcher_career_stat_data,'pitcher_career_stats') # Pitcher career
write_csv(hitter_stat_data,'hitter_stats') # Hitter
write_csv(bullpen_stat_data,'bullpen_stats') # Bullpen
write_csv(team_batting_stat_data,'team_batting_stats') # Team Batting
