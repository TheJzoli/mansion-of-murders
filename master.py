import random

import sql
import move
import look
import ask
#import blame

# This controls text output beyond vanilla print
def fprint (text):
	# Obviously its not implemented yet
	print (text)
	
# This is just to make debug messages stand out, in code and output
def DEBUG (message):
	print ("DEBUG: " + str(message))
	
def shuffle (list):
	count = len(list)
	for i in range (count - 1):
		random_index = random.randint(i, count - 1)
		list[i], list[random_index] = list[random_index], list[i]
	
## VOCABULARY
# Get verbs and prepositions from database
verbs = sql.get_verbs()
prepositions = sql.get_prepositions()

# Get targets as well. Also store them in invidual arrays to further parse commands. 
rooms = sql.get_rooms()

# sql.get_npcs returns a list where [0] is first names and [1] is last names
sql_npcs = sql.get_npcs_names()
first_names = sql_npcs [0]
last_names = sql_npcs [1]
npcs = sql.get_npcs()

# sql.get_directions returns list, [0] is shortcut, [1] is full name
directions = sql.get_directions()
short_directions = directions [0]
long_directions = directions [1]
directions = short_directions + long_directions

targets = rooms + npcs + directions
DEBUG ("targets: " + str(targets) + "\n")



## INITIALIZE MOVE
move.rooms = rooms
move.directions = directions
move.short_directions = short_directions
move.long_directions = long_directions


## INITIALIZE LOOK
look.rooms = rooms
look.npcs = npcs
look.first_names = first_names
look.last_names = last_names
look.directions = directions


## INITIALIZE ASK


## INITIALIZE PLAYER ==========================================================
class Player():
	location = 1
	
# Start at full used actions, so that npcs will move on first turn
player_actions = 3
player_actions_used = player_actions

player = Player()
move.player = player
look.player = player
ask.player = player
#blame.player = player

## INITIALIZE NPCS ============================================================
npcs_amount = len(first_names)
npc_ids = []
for i in range(npcs_amount):
	npc_ids.append(i + 1)
shuffle (npc_ids)

rooms_amount = len(rooms)
room_ids = []
for i in range(rooms_amount):
	room_ids.append (i + 1)
shuffle (rooms)

murder_sub_A = random.randint(1, 5)
murder_sub_B = random.randint(1, 5)
possible_murderers = sql.get_murderers(murder_sub_A, murder_sub_B)
shuffle (possible_murderers)

number_murderers = int(npcs_amount / 10)
selected_murderers = possible_murderers [:number_murderers]

sql.map_npcs(npc_ids, room_ids, selected_murderers)


## INITIALIZE MURDERS ========================================================
# First murder must happen in entrance, so that player finds it early
first_murderer = sql.query_single("SELECT MIN(mapped_id) FROM mapped_npc WHERE state = 'murdering';")
DEBUG ("First murderer is {0}.".format(sql.npc_name_from_id(first_murderer)))
sql.move_npc(first_murderer, sql.room_id_from_name('entrance'))

# Still start murderer index from 0
current_murderer_id = 0

## GAME LOOP ==================================================================
round = 0
playing = True
while (playing):
	
	# Check if its time for npcs to do npc things
	if player_actions_used == player_actions:
		player_actions_used = 0
		round += 1
		
		fprint("------------ Round {0} --------------".format(round))

		# Find murderer -------------------------------------------------------
		murderers = sql.get_active_murderers()

		next_murderer_id = None
		for npc in murderers:
			if npc > current_murderer_id:
				next_murderer_id = npc
				break
		
		if next_murderer_id == None:
			current_murderer_id = murderers[0]
		else:
			current_murderer_id = next_murderer_id
		
		# Find victim ---------------------------------------------------------
		possible_targets = sql.get_targets(current_murderer_id)
		
		if possible_targets != None:
			victim_id = random.choice(possible_targets)
			
			murderer_location = sql.get_npc_location (current_murderer_id)
			victim_location = sql.get_npc_location(victim_id)
			sql.move_npc(current_murderer_id, victim_location)
			
			if victim_location != murderer_location:
				DEBUG ("Murderer {0} moved from {1} to {2} to kill {3}!".format(sql.npc_name_from_id(current_murderer_id), sql.room_name_from_id(murderer_location), sql.room_name_from_id(victim_location), sql.npc_name_from_id(victim_id)))
			else:
				DEBUG ("Murderer {0} killed {1} in {2}!".format(sql.npc_name_from_id(current_murderer_id), sql.npc_name_from_id(victim_id), sql.room_name_from_id(victim_location)))
			
			sql.murder(victim_id, current_murderer_id)
		
		else:
			DEBUG("No targets left for remaining killer {0}.".format(sql.npc_name_from_id(current_murderer_id)))
			
		# Clues ---------------------------------------------------------------
		if victim_id:
			DEBUG ("{0} was killed".format(sql.npc_name_from_id(victim_id)))
			clues = sql.get_details(current_murderer_id);
			shuffle(clues)
			witnesses = sql.live_npcsid_in_room(sql.get_npc_location(current_murderer_id))
			if current_murderer_id in witnesses:
				witnesses.remove (current_murderer_id)
			shuffle(witnesses)
			
			if len(witnesses) > 0:
				for i in range (5):
					clue = clues [i]
					witness_id = witnesses [i % len(witnesses)]
					sql.add_clue (victim_id, witness_id, clue)
	#				DEBUG("Added clue {0} to {1}.".format(sql.detail_name_from_id(clue), sql.npc_name_from_id(witness_id)))
			else:
				DEBUG ("No witnesses")
			
		# Reset killing -------------------------------------------------------
		victim_id = None
		
		# Npcs move -----------------------------------------------------------
		living_npcs = sql.get_living_npcs()
		for npc in living_npcs:
			do_move = random.choice([True, False])
			if do_move:
				destination = random.choice(sql.get_npc_possible_directions(npc))
				sql.move_npc(npc, destination)
	
	
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
		next_word = None
		
		# Don't look last word, since it can't be first of two part word ------
		if index < word_range - 1:
			next_word = raw_command [index + 1]
			parts = sql.get_two_part_words(word)
			if parts != None and next_word in parts:
				command_word = "{0} {1}".format(word, next_word)
				index += 1
			
			else:
				command_word = word
		
		else:
			command_word = word
		

		# Check for synonyms --------------------------------------------------
		command_word = sql.get_word_from_synonym(command_word)
		
		# Check for full name after synonyms ----------------------------------
		if command_word in first_names and next_word == sql.get_last_name(command_word):
			command_word = command_word, next_word
			DEBUG ("phase 1: " + str(command_word))
			index += 1
			
		elif command_word in first_names or command_word in last_names:
			first_name = None
			last_name = None

			for i in range(len(first_names)):
				
				if command_word == first_names [i]:
					first_name = command_word
					if last_name is None:
						last_name = last_names [i]
					else:
						last_name = False
						
				elif command_word == last_names [i]:
					last_name = command_word
					if first_name is None:
						first_name = first_names[i]
					else:
						first_name = False		
				
			command_word = first_name, last_name
			DEBUG ("cmd test: " + str(command_word))
		# ---------------------------------------------------------------------
		
		command.append (command_word)
		index += 1
	# End of command process loop ---------------------------------------------
	
	# Parse command -----------------------------------------------------------
	verb = None
	target1 = None
	preposition = None
	target2 = None
	
	for word in command:
		
		if verb is None:
			if word in verbs:
				verb = word
				
		
		elif word in directions:
				target1 = word
		
		elif preposition is None:
			
			if word in targets and target1 is None:
				target1 = word
				
			elif word in prepositions:
				preposition = word
				
		elif target2 is None:
			
			if word in targets:
				target2 = word
				

	DEBUG ("{0} {1} {2} {3}".format(verb, target1, preposition, target2))
				
	# Check if player entered only direction ----------------------------------
	if target1 in long_directions:
		target1 = sql.short_direction(target1)
	
	if verb == None and target1 in directions:
		verb = 'move'
		
	# Build SQL-query from parsed commands ------------------------------------
	if verb:
		# verb ----------------------------------------------------------------
		query = "SELECT id FROM actions WHERE verb = '{0}'".format(verb)
		
		# preposition ---------------------------------------------------------
		if (preposition):
			query += " AND preposition = '{0}'".format(preposition)
		else:
			query += " AND preposition IS NULL"
		
		# targets ------------------------------------------------------
		if target1:
			has_target1 = True
		else:
			has_target1 = False
		query += " AND has_target1 = {0}".format(has_target1)
			
			
		if target2:
			has_target2 = True
		else:
			has_target2 = False
		query += " AND has_target2 = {0}".format(has_target2)
		
		#---------------------------------------------------------------
		query += ";"
		

		# Get Action id
		action = sql.query_single(query)
		
		# Do action, and spend action points
		if (action):
			super = int(action / 10)
			sub = action - super * 10
			
			# DEBUG("super: {0}, sub: {1}".format(super, sub))
			use_action_point = False
			if super == 1: # MOVE
				fprint(move.move(target2))
				use_action_point = True
				
			elif super == 2: # LOOK
				if sub == 0:
					fprint(look.look(target2))
				
				elif sub == 1:
					fprint(look.look_around())
		
			elif super == 3: # ASK
				fprint(ask.ask(target1, target2))
				use_action_point = True
			
			elif super == 9: # WAIT
				fprint ("Some time passes.")
				use_action_point = True
				
			if use_action_point:
				player_actions_used += 1
			
	else:
		fprint("There was no verb, what do you want to do?")
			


	
## END GAME LOOP	
	
sql.end()



