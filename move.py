import sql

def move(room_name):
	if (room_name in sql.get_adjacent_rooms(room_name)):
		current_room = sql.get_room_id(room_name)
		fprint("Move to {0}".format(sql.get_room_name(room_id)))
		return True
	else:
		fprint("You can't go there from here!")
		return False