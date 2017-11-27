'''
# These are all populated from master.py
rooms = [] 				# Names of rooms
directions = []			# Directions' names and shortcuts
short_directions = [] 	# Directions ids
long_directions = [] 	# Full names of directions
'''
import sql

current_room = 1

def move(target):
	message = ""
	if target in rooms:
		target_room_id = sql.get_room_id(target)
		adjacent_rooms = sql.get_adjacent_rooms(current_room)
		if target_room_id in adjacent_rooms:
			current_room = target_room_id
			message = 'Moved to {0}'.format(target)
		'''
		else
	elif target in directions:
		query =
		
	else:
		'''
	
	
	
	
	
	
	return message