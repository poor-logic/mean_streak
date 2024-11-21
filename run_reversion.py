import csv
import requests
from bs4 import BeautifulSoup
import time
from web_extract import *

team_names = {'CHW': 'Chicago White Sox',
              'STL': 'St. Louis Cardinals',
              'PHI': 'Philadelphia Phillies',
              'PIT': 'Pittsburgh Pirates',
              'CIN': 'Cincinnati Reds',
              'LAD': 'Los Angeles Dodgers',
              'LAA': 'Los Angeles Angels',
              'SDP': 'San Diego Padres',
              'WSN': 'Washington Nationals',
              'ATL': 'Atlanta Braves',
              'COL': 'Colorado Rockies',
              'TOR': 'Toronto Blue Jays',
              'SFG': 'San Francisco Giants',
              'MIA': 'Miami Marlins',
              'NYM': 'New York Mets',
              'TEX': 'Texas Rangers',
              'MIL': 'Milwaukee Brewers',
              'BOS': 'Boston Red Sox',
              'BAL': 'Baltimore Orioles',
              'ARI': 'Arizona Diamondbacks',
              'DET': 'Detroit Tigers',
              'NYY': 'New York Yankees',
              'OAK': 'Oakland Athletics',
              'MIN': 'Minnesota Twins',
              'SEA': 'Seattle Mariners',
              'KCR': 'Kansas City Royals',
              'HOU': 'Houston Astros',
              'TBR': 'Tampa Bay Rays',
              'CHC': 'Chicago Cubs',
              'CLE': 'Cleveland Guardians',
              }
              
              
HEADERS = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", 
  }
  
 
# Function to grab individual team schedules/scores from baseball reference    
def get_schedule(team_url):   
    baseball_ref_schedule = get_html(f'https://www.baseball-reference.com/teams/{team_url}/2024-schedule-scores.shtml')
    table = baseball_ref_schedule.find('div', id="all_team_schedule")
    rows = table.find_all('tr')

    data_sheet = []
    for row in rows:
        row_list = []
        for item in row:
            row_list.append(item.text.strip())
        team = row_list[3]
        runs = row_list[7]
        runs_against = row_list[8]
    
        if row_list[2] == 'boxscore':
            data_sheet.append([team, runs, runs_against])
    
    return data_sheet


# Function to get the average runs and runs against of the last n games
def last_n_games(team, num_of_games):
    
    # Set running variables
    total_runs = 0
    total_runs_against = 0
    runs = 0
    runs_against = 0
    name = ''
    
    # Each row represents one game for given team
    # Calculate team average for last n games(num_of_games) for runs scored and runs against
    for row in team[-int(f'{num_of_games}'):]:
        runs = runs + int(row[1])
        runs_against = runs_against + int(row[2])
        name = team_names[row[0]]
    
    # Calculate team season averages for runs scored and runs against
    for row in team:
        total_runs = total_runs + int(row[1])
        total_runs_against = total_runs_against + int(row[2])
        
    return [name,round(total_runs/len(team),2), round((runs/num_of_games) - total_runs/len(team),2), round(total_runs_against/len(team),2),round((runs_against/num_of_games) - total_runs_against/len(team),2)]

# Iterate through the all schedules and run last_n_games() on each schedule
# Return a csv ready list that contains lists of each teams last_n_games() data
def n_game_average(num_of_games):
    csv_data = [['Team Run Average Reggression'],['Team', 'Season Avg. R', f'{num_of_games} Game Avg. R', 'Season Avg. RA', f'{num_of_games} Game Avg. RA']]

    for schedule in schedules:
        last_n = last_n_games(schedule, num_of_games)
        csv_data.append(last_n)   
        
    return csv_data


# Code Execution
schedules = []
for team in team_names.keys():
    schedule = get_schedule(team)
    schedules.append(schedule)
    time.sleep(2)


ranges = [3, 5, 10]
for num in ranges:
    average = n_game_average(num)
    write_csv(average, f'run_reversion_{num}')