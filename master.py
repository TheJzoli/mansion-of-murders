import sql
import look

# This controls text output beyond vanilla print
def fprint (text):
	# Obviously its not implemented yet
	print (text)
	
# This is just to make debug messages stand out, in code and output
def DEBUG (message):
	print ("DEBUG: " + str(message))
	
## VOCABULARY
# Get verbs and prepositions from database
verbs = sql.get_verbs()
prepositions = sql.get_prepositions()

# Get targets as well. Also store them in invidual arrays to further parse commands. 
rooms = sql.get_rooms()

# sql.get_npcs returns a list where [0] is first names and [1] is last names
npcs = sql.get_npcs()
first_names = npcs [0]
last_names = npcs [1]
npcs = first_names + last_names

# sql.get_directions returns list, [0] is shortcut, [1] is full name
directions = sql.get_directions()
short_directions = directions [0]
long_directions = directions [1]
directions = short_directions + long_directions

targets = rooms + npcs + directions
DEBUG (targets)

## INITIALIZE MOVE
import move
move.rooms = rooms
move.directions = directions
move.short_directions = short_directions
move.long_directions = long_directions

## INITIALIZE LOOK

## GAME LOOP
playing = True
while (playing):

	# Take input
	command = input (">>").lower().split()

	# Parse input
	verb = None
	preposition = None
	target = None
	
	for word in command:
	
		if verb == None:
			if word in verbs:
				verb = word
			
			elif word in directions:
				target = word
			
		elif target == None:
		
			if word in targets:
				target = word
			
			elif preposition == None and word in prepositions:
				preposition = word
	
	
	# Check if player entered only direction
	if target in long_directions:
		target = sql.short_direction(target)
	
	if verb == None and target in directions:
		verb = 'move'
		
	# Build SQL-query from parsed commands
	if verb:
		# verb ----------------------------------------------------------
		query = "SELECT id FROM actions WHERE verb = '{0}'".format(verb)
		
		# preposition --------------------------------------------------
		if (preposition):
			query += " and preposition = '{0}'".format(preposition)
		else:
			query += " and preposition IS NULL"
		
		# target -------------------------------------------------------
		if target:
			has_target = True
		else:
			has_target = False
		query += " and has_target = {0}".format(has_target)
		
		#---------------------------------------------------------------
		query += ";"
		
		action = sql.query_single(query)
		DEBUG("Action: " + str(action))
		
	else:
		fprint("There was no verb, what do you want to do?")
			
	DEBUG ("{0} {1} {2}".format(verb, preposition, target))

sql.end()
