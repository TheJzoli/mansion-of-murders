import sql

Look = ['look', 'eye', 'glance', 'glimpse', 'peek', 'view', 'gander', 'gaze', 'inspect', 'leer', 'observe', 'watch']


def show_room (room_id):
	message = "You are in {0}.\n".format (sql.get_room_name(room_id))
	adjacent_rooms = sql.get_adjacent_rooms(room_id)
	for id in adjacent_rooms:
		message += "\t{0}".format(sql.get_room_name(id))
	return message