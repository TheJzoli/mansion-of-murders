# Color ansi escapes
cmd_colour = '\x1b[93m'
default_colour = '\x1b[97;100m'
expired_colour = '\x1b[37m'

## Player section =============================================================
class Player():
	location = 1

player = Player()

## DEBUG section ==============================================================
from inspect import getframeinfo, stack
debug = True
def DEBUG (message):
	if debug:
		caller = getframeinfo(stack()[1][0])
		print ("DEBUG [{0}: {1}]: {2}".format(caller.filename.split(sep="\\")[-1], caller.lineno, message))


## Format section =============================================================
def format_npc (name):
	namestr = name[0].title() + " " + name[1].title()
	return namestr

def format_room (room):
	return room.title()
	
	# Joel tää palauttaa joistain Nonen, ei käy
	# ainakin music room
	roomstr = room.title()
	roomlist = roomstr.split()
	if (roomlist[0][-1] == 's'):
		room0 = list(roomlist[0])
		room0.insert(-1, "'")
		roomstring0 = "".join(room0)
		#print(roomstring0 + " " + roomlist[1])
		return roomstring0 + " " + roomlist[1]
	if (len(roomlist) >= 2 and roomlist[1][-1] == 's'):
		room1 = list(roomlist[1])
		room1.insert(-1, "'")
		roomstring1 = "".join(room1)
		#print(roomlist[0] + " " + roomstring1)
		return roomlist[0] + " " + roomstring1
	if (len(roomlist) == 1):
		return roomstr
		
'''
print(room("gallery"))
print(room("music room"))
print(room("butlers room"))
'''