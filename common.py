from random import randint
from inspect import getframeinfo, stack

# Color ansi escapes
cmd_colour = '\x1b[93m'
default_colour = '\x1b[97;100m'
expired_colour = '\x1b[37m'

## DEBUG section ==============================================================
debug = True
def DEBUG (message):
	if debug:
		caller = getframeinfo(stack()[1][0])
		print ("DEBUG [{0}: {1}]: {2}".format(caller.filename.split(sep="\\")[-1], caller.lineno, message))

## Utilities ==================================================================
def shuffle (list):
	count = len(list)
	for i in range (count - 1):
		random_index = randint(i, count - 1)
		list[i], list[random_index] = list[random_index], list[i]

def safe_remove(value, list):
	value in list and list.remove(value)


## Player section =============================================================
class Player():
	location = 1

player = Player()



## Format section =============================================================
def format_npc (name):
	namestr = name[0].title() + " " + name[1].title()
	return namestr

def format_room (room):
	roomstr = room.title()
	roomlist = roomstr.split()

	if (roomlist[0][-1] == 's'):
		room0 = list(roomlist[0])
		
		if (roomlist[0] == 'Servants'):
			room0.append("'")
			roomstring0 = "".join(room0)
			return roomstring0 + " " + roomlist[1]
			
		else:
			room0.insert(-1, "'")
			roomstring0 = "".join(room0)
			return roomstring0 + " " + roomlist[1]
			
	if (len(roomlist) >= 2 and roomlist[1][-1] == 's'):
		room1 = list(roomlist[1])
		room1.insert(-1, "'")
		roomstring1 = "".join(room1)
		return roomlist[0] + " " + roomstring1
		
	return roomstr
		
def format_list (collection, formatter):	
	if not collection:
		result = None
	
	else:
		count = len(collection)
	
		if count == 1:
			result = formatter(collection [0])
		
		else:
			result = ""
			for i in range (count - 2):			
				item = formatter(collection[i])
				result += "{0}, ".format(item)
					
			second_last = formatter(collection[-2])
			last = formatter(collection[-1])
			result += "{0} and {1}".format(second_last, last)
				
	return result		
	
'''	
def direction (dir):
	direction = sql.long_direction(dir)
	return direction
'''

'''
print(format_room("maids room"))
print(format_room("servants room"))
print(format_room("butlers room"))
'''