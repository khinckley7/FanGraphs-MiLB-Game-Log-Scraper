from bs4 import BeautifulSoup
import pandas as pd
import urllib
from datetime import datetime, timedelta
import urllib.request
import csv
# import webbrowser
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

# Open THE BOARD (2019) 
file =  open('theboard2019.csv', 'r')

# Read csv file
reader = csv.reader(file)
next(reader) # Skips headers

players = {} # Create dictionary of players to store id, position, and FV

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
	players[row[2].lower()] = {'id': row[20], 'position':pos, 'FV':row[9]}

today = datetime.now() 
start_date = (today - timedelta(days=365)).date() # 365 days prior
today = today.strftime('%Y-%m-%d') # Today's date



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
			col_names.append(col_name)

		for col in table.select('td'):
			col = str(col)
			stat = strip_tags(col)
			stats.append(stat)


		game_log = pd.DataFrame(list(zip(col_names, stats)), columns=[player_name,str(start_date)+'-'+str(end_date)])
		print(game_log)

	except:
		pass


for key, value in players.items():
	
	player_name = key
	player_id = value['id']
	position = value['position']
	FV = value['FV']


	milb_game_logs(player_name, player_id, position, start_date, today)

# milb_game_logs("aj-puk", "19343", "P", start_date, today)
