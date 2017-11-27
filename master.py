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

	# Receive and process input
	# Get input, lower and split it
	# Look for two part words
	# Look for synonyms, and swap
	raw_command = input (">>").lower().split()
	command = []
	word_range = len(raw_command)
	index = 0
	while index < word_range:
		word = raw_command[index]
		
		if index < word_range - 1:
			next = raw_command [index + 1]
			
			parts = sql.get_two_part_words(word)
			if parts != None and next in parts:
				command_word = "{0} {1}".format(word, next)
				index += 1
			
			else:
				command_word = word
		
		else:
			command_word = word
		
		# Check for synonyms
		command_word = sql.get_word_from_synonym(command_word)
		
		command.append (command_word)
		index += 1
	# End of command process loop
	
	print(command)
	
	
	# Parse input
	verb = None
	target1 = None
	preposition = None
	target2 = None
	
	for word in command:
		
		if verb == None:
			if word in verbs:
				verb = word
				
			elif word in directions:
				target1 = word
		
		elif preposition == None:
			
			if word in targets and target1 == None:
				target1 = word
				
			elif word in prepositions:
				preposition = word
				
		elif target2 == None:
			
			if word in targets:
				target2 = word
				DEBUG("target2: " + word)
				
				
	# Check if player entered only direction
	if target1 in long_directions:
		target1 = sql.short_direction(target1)
	
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
			
	DEBUG ("{0} {1} {2} {3}".format(verb, target1, preposition, target2))

	# Update location
	look.current_room = move.current_room
## END GAME LOOP	
	
sql.end()








