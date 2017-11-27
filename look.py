'''
# These are all populated from master.py
rooms = [] 				# Names of rooms
npcs = []
first_names = []
last_names = []
'''

def look (target):
	if target:
		return "You look at {0}".format (target)
	else:
		return "You look around"