'''
# These are all populated from master.py
player					# Instance of Player class
rooms = [] 				# Names of rooms
directions = []			# Directions' names and shortcuts
short_directions = [] 	# Directions ids
long_directions = [] 	# Full names of directions
'''
import sql
import webbrowser
print("INIT MOVE")


def move(target):
	message = ""
	if target in rooms:
		target_room_id = sql.get_room_id(target)
		adjacent_rooms = sql.get_adjacent_rooms(player.location)
		if target_room_id in adjacent_rooms:
			player.location = target_room_id
			message = 'Moved to the {0}'.format(target)
		else:
			message = "You can't move there!"
	elif target in directions:
		available_directions = sql.get_available_directions(player.location)
		if target in available_directions:
			target_room = sql.get_target_room_id(target)
			player.location = target_room
			message = 'Moved to the {0}'.format(sql.get_room_name(player.location))
		else:
			message = "You can't move there!"
	elif target == 'hell':
		webbrowser.open_new('https://www.youtube.com/watch?v=l482T0yNkeo')
	else:
		message = "That is not somewhere you can go!"
	return message