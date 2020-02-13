from bs4 import BeautifulSoup
import pandas as pd
import urllib
from datetime import datetime, timedelta
import urllib.request
import csv
from html.parser import HTMLParser

# Create HTML stripper
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

# HTML stripping function
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# Open THE BOARD 
THEBOARD = pd.read_csv('theboard2020.csv') 

THEBOARD = THEBOARD.replace({'Pos': {'RHP': 'P', 'LHP': 'P', 'LF': 'OF', 'CF': 'OF', 'RF': 'OF'}}) # Re-code position labels

THEBOARD['Name'] = THEBOARD['Name'].str.lower() # Change names to lowercase
THEBOARD['Name'] = THEBOARD['Name'].str.replace('.','') # Erase periods from names
THEBOARD['Name'] = THEBOARD['Name'].str.replace(' ','-') # Repalce spaces with hypens

THEBOARD = THEBOARD[['Name', 'Org', 'Pos', 'Current Level', 'FV', 'ETA', 'Age', 'playerId']] # Keep only relevant columns

player_dict = THEBOARD.set_index('Name').T.to_dict('list') # Convert THEBOARD dataframe into dictionary

today = datetime.now() # Get today's date
start_date = (today - timedelta(days=218)).date() # 365 days prior
today = today.strftime('%Y-%m-%d') # Today's date (formatted) 


def milb_game_logs(player_name, player_id, position, start_date, end_date=today):

	base = 'https://www.fangraphs.com/players/'

	# Advanced stats table
	url = base + str(player_name) + '/' + str(player_id) + '/game-log?position=' + str(position) + '&gds=' + str(start_date) + '&gde=' + str(end_date) + '&season=&type=-2'

	try:
		page = urllib.request.urlopen(url)
		soup = BeautifulSoup(page, 'lxml')
		table = soup.find('table', class_='rgMasterTable') # Store table

		col_names = []
		stats = []

		for col in table.select('th'):
			col = str(col)
			col_name = strip_tags(col)
			col_names.append(col_name) # Add column name

		for col in table.select('td'):
			col = str(col)
			stat = strip_tags(col)
			stats.append(stat) # Add stat value


		game_log = pd.DataFrame(list(zip(col_names, stats)), columns=[player_name,str(start_date)+'-'+str(end_date)])
		# print(game_log)
		return game_log

	except:
		pass

game_logs = pd.DataFrame() # Create empty dataframe to store game logs

# Loop through THEBOARD
for key, value in player_dict.items():
	
	player_name = key
	organization = value[0]
	position = value[1]
	level = value[2]
	FV = value[3]
	ETA = value[4]
	age = value[5]
	player_id = value[6]
	
	if position != 'P' and level == 'AA':
		milb_game_logs(player_name, player_id, position, start_date, today)
		# game_logs = game_logs.append(milb_game_logs(player_name, player_id, position, start_date, today), sort=True)

# Test
# milb_game_logs("aj-puk", "19343", "P", start_date, today)



