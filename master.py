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
sql_npcs = sql.get_npcs()
first_names = sql_npcs [0]
last_names = sql_npcs [1]
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
import look
look.npcs = npcs



## INITIALIZE PLAYER
move.current_room = 1

## GAME LOOP
playing = True
while (playing):

	# Take input
	command = input (">>").lower().split()
	'''
	range = len(command) - 2
	i = 0
	while i < range:
		parts = sql.get_two_part_words(command[i])
		if command [i + 1] in parts:
			command[i] += " " + command[i+1]
			del command[i+1]
			range -= 1
		else:
			i + 1
		
	print(command)
	'''
	
	# Parse input
	verb = None
	target1 = None
	preposition = None
	target2 = None
	
	for word in command:
	
		if verb == None:
			if word in verbs:
				verb = word
			
			# Direction only is enough too
			elif word in directions:
				target1 = word
			
		elif target1 == None:
		
			if word in targets and preposition == None:
				target1 = word
			
			elif preposition == None and word in prepositions:
				preposition = word
		
	
	# Check if player entered only direction
	if target1 in long_directions:
		target = sql.short_direction(target)
	
	if verb == None and target1 in directions:
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
		if target1:
			has_target = True
		else:
			has_target = False
		query += " and has_target = {0}".format(has_target)
		
		#---------------------------------------------------------------
		query += ";"
		
		action = sql.query_single(query)
		DEBUG(query)
		DEBUG("Action: " + str(action))
		
		if (action):
			super = int(action / 10)
			sub = action - super
			
			if super == 1:
				fprint(move.move(target1))
				
			if super == 2:
				fprint(look.look(target1))
		
		
		
	else:
		fprint("There was no verb, what do you want to do?")
			
	DEBUG ("{0} {1} {2}".format(verb, preposition, target1))

	# Update location
	look.current_room = move.current_room
## END GAME LOOP	
	
sql.end()






'''

### move
def move(place, item, person):

input = "Move Jack to Mountain"

place = "Mountain"
item = None
person = "Jack"

verb = "move"


sql_result = do_sql_stuff(verb)

#result = "move"

method = getattr(self, verb)

method (target1, target2, target3)

'''








