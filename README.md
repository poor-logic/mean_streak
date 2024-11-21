# mean_streak
Mean Streak is a system designed to assist in the prediction of runs scored in MLB games. It centers around a 'reversion to the mean' strategy, while considering other factors such as pitchers and run efficiency.

***Disclaimer***
This is meant as an experiment in data analytics. This is NOT gambling advice. If you choose to deploy this system to place wagers, you do so at your own risk.


The Theory
----------
The idea behind Mean Streak is that no streak lasts forever and the longer one continues, the more likely it is to end. In other words, eventually you will see a reversion to the mean. The way this is achieved can be demonstrated in the following steps:

1) Calculate each team’s average runs p/game
2) Calculate each team’s average runs p/game over the last_n_number_of_games
3) Calculate the difference to see how far behind or ahead of the season average the team in the last_n_number_of_games

* The same steps are followed for runs against p/game

From these calculations, we can see how a team is faring by comparing their season average to the last_n_number_of_games average. If there is a significant difference between the numbers (an absolute value of 2 or more), it may be an indicator that a reversion is imminent. 


Modules
-------
**games_to_csv**<br/>
This module interacts with the mlb.com API and retrieves the MLB games for today. After it retrieves the games, it writes the game schedule to a csv file (games.csv) in the Data folder.

**stats_to_csv**<br/>
This module interacts with the mlb.com API to retrieve stats and write each set of stats into its own csv file in the Data folder. 

**run_reversion**<br/>
This module scrapes baseball-reference.com for schedules and scores for each team. It then calculates the run and runs against averages for the last_n_games and writes it to a csv file(run_reversion_{num}) in the Data folder. The module default will produce 3 csv files. One each for the last 3, 5, and 10 games.

**web_extract**<br/>
This module contains functions for retrieving files from the internet and writing csv files to the machine.


Data Folder
-----------
The data folder is where all processed data is stored. The input folder contains data keys for the json files provided by the mlb.com API. Each file in the input folder contains a complete list of all possible keys for the given json. All keys were included for the sake of reference. Not all keys are needed. The clean_labels.txt file acts as a legend for all keys.


Tools
-----
The file mlb_daily_report.xlsx is the system dashboard. After all scripts run, open this file and refresh all data. Here, you will be able to compare matchup data by comparing pitching matchups, 3, 5 and 10 game run averages, team run % (runs/baserunners) and opposing bullpen stats.

* Run averages are displayed as distance from season average (example: -2.3 represents 2.3 runs under season average over given stretch)

* All data tabs are hidden. You can view them by right clicking on the Report tab and selecting unhide.


Execution
---------
1) run main.py
2) open mlb_daily_report.xlsx and refresh all data


Notes
-----
- Included in the initial commit are all the processed csv files for the end of the 2024 season. These were left to provide data to the mlb_daily_report.xlsx file so as to provide an example of the dashboard visualization.

- The run_reversion and stats_to_csv modules are automatically set to current year. The games_to_csv module is automatically set for todays date. To configure this, you will need to go into each module and edit the dates within each url to run the script for custom dates.

- There are 3 third party libraries used within the Python files and will need to be installed before the files are run:
  1) BeautifulSoup
  2) Pandas
  3) Unidecode
