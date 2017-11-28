'''
# These are all populated from master.py
rooms = [] 				# Names of rooms
directions = []			# Directions' names and shortcuts
short_directions = [] 	# Directions ids
long_directions = [] 	# Full names of directions
'''
import sql
print("INIT MOVE")

current_room = 1

def move(target):
	message = ""
	if target in rooms:
		target_room_id = sql.get_room_id(target)
		adjacent_rooms = sql.get_adjacent_rooms(current_room)
		if target_room_id in adjacent_rooms:
			current_room = target_room_id
			message = 'Moved to the {0}'.format(target)
		else:
			message = "You can't move there!"
	elif target in directions:
		available_directions = sql.get_available_directions(current_room)
		if target in available_directions:
			target_room = sql.get_target_room_id(target)
			current_room = target_room
			message = 'Moved to the {0}'.format(sql.get_target_room_name)
		else:
			message = "You can't move there!"
	else:
		message = "That is not somewhere you can go!"
	return message