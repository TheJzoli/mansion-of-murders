import sql

def name (name):
	namestr = name[0].title() + " " + name[1].title()
	return namestr

def room (room):
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
	return roomstr

def direction (dir):
	direction = sql.long_direction(dir)
	return direction