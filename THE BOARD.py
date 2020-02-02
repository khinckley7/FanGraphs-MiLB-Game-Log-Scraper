from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib
from datetime import datetime
import urllib.request
import csv
import webbrowser

# Open THE BOARD (2019) 
file =  open('theboard2019.csv', 'r')

# Read csv file
reader = csv.reader(file)
next(reader) # Skips headers

players = {} # Create dictionary of players to store id and position

# Iterate through csv file
for row in reader:

	# Standardize position markers
	if row[4] == 'RHP' or row[4] == 'LHP':
		pos = 'P'
	elif row[4] =='RF' or row[4] =='CF' or row[4] =='LF':
		pos = 'OF'
	else:
		pos = row[4]

	# Add entry to dictionary
	players[row[2].lower()] = {'id': row[20], 'position':pos}

today = datetime.today().strftime('%Y-%m-%d') # Today's date

def milb_game_logs(player_name, player_id, position, start_date=0000-00-00, end_date=today):

	base = 'https://www.fangraphs.com/players/'

	# Advanced stats table
	url = base + str(player_name) + '/' + str(player_id) + '/game-log?position=' + str(position) + '&gds=' + str(start_date) + '&gde=' + str(end_date) + '&season=&type=-2'
	# print(url)
	# webbrowser.open(url)

	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, 'lxml')
	table = soup.find('table', class_='rgMasterTable') # Store table

	for col in table.select('th'):
		matches = re.findall('(,d">)(\\S*)(<\\/a>)', col)
		print(matches)

# for key, value in players.items():
	
# 	player_name = key
# 	player_id = value['id']
# 	position = value['position']
	
# 	milb_game_logs(player_name, player_id, position, 0000-00-00, today)

milb_game_logs("aj-puk", "19343", "P", 0000-00-00, today)





