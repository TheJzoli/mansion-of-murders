import random

import sql
import move
import look
import ask
import blame
import formatter

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

	

	
## VOCABULARY =================================================================
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

specials = sql.get_specials()
targets = rooms + npcs + directions + specials

## PARSER CONTEXTS ============================================================
no_context_query = "SELECT {0} FROM npc WHERE {1} = '{2}';"
context_room_query = (
					"SELECT {0} FROM npc "
					"INNER JOIN mapped_npc ON mapped_npc.npc = npc_id "
					"WHERE {1} = '{2}' AND location = {3};"
					)
context_clue_query = (
					"SELECT {0} FROM npc "
					"INNER JOIN mapped_npc ON mapped_npc.npc = npc_id "
					"INNER JOIN clue ON victim = mapped_id "
					"WHERE {1} = '{2}' AND witness = {3};"
					)
context_murder_query = (
					"SELECT {0} FROM npc "
					"INNER JOIN mapped_npc ON mapped_npc.npc = npc_id "
					"INNER JOIN murder ON victim = mapped_id "
					"WHERE {1} = '{2}' AND murderer = {3};"
					)

def find_other_name(context, known):		

	if known in first_names:
		known_str = 'first_name'
		unknown_str = 'last_name'
	else:
		known_str = 'last_name'
		unknown_str = 'first_name'
		
	if context is None:
		unknown_query = no_context_query.format(unknown_str, known_str, known)
	elif context[0] == 'room':
		unknown_query = context_room_query.format(unknown_str, known_str, known, context[1])
	elif context[0] == 'clue':
		unknown_query = context_clue_query.format(unknown_str, known_str, known, context[1])
	elif context[0] == 'murder':
		unknown_query = context_murder_query.format(unknown_str, known_str, known, context[1])
		
	unknown_names = sql.column_as_list(sql.run_query(unknown_query), 0)
	
	if len(unknown_names) == 1:
		unknown = unknown_names [0]
	elif context is None:
		unknown = None
	elif context[0] in ['clue', 'murder']:
		unknown = find_other_name(['room', player.location], known)
	elif context[0] == 'room':
		unknown = find_other_name (None, known)
	else:
		#this shouldn't ever occur
		DEBUG ("Context WTF?")
		unknown = None
	
	return unknown

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

def npc_move_message (moving_npcs, action):
	move_message = ""
	
	if action == 'enter':
		action_str = 'entered'
		preposition = ' from'
	elif action == 'exit':
		action_str = 'exit'
		preposition = 'to'
	
	current_room = sql.room_name_from_id(player.location)
	for item in moving_npcs:
		name = formatter.name(sql.npc_name_from_id(item[0]))
		other_room = sql.room_name_from_id(item[1])
		move_message += "{0} has {1} the {2} {3} the {4}.\n".format(
														name,
														action_str,
														current_room,
														preposition,
														other_room
														)
	
	return move_message


## INITIALIZE MURDERS ========================================================
# First murder must happen in entrance, so that player finds it early
# It is enough to move the first murderer there, because all npcs are dealt evenly across rooms
first_murderer = sql.query_single("SELECT MIN(mapped_id) FROM mapped_npc WHERE state = 'murdering';")
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
		
		DEBUG("------------ Round {0} --------------".format(round))
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
		'''	
			if victim_location != murderer_location:
				DEBUG ("Murderer {0} moved from {1} to {2} to kill {3}!".format(sql.npc_name_from_id(current_murderer_id), sql.room_name_from_id(murderer_location), sql.room_name_from_id(victim_location), sql.npc_name_from_id(victim_id)))
			else:
				DEBUG ("Murderer {0} killed {1} in {2}!".format(sql.npc_name_from_id(current_murderer_id), sql.npc_name_from_id(victim_id), sql.room_name_from_id(victim_location)))

		else:
			DEBUG("No targets left for remaining killer {0}.".format(sql.npc_name_from_id(current_murderer_id)))
		'''
			
		# Npcs move -----------------------------------------------------------
		living_npcs = sql.get_living_npcs()
		living_npcs.remove(current_murderer_id)
		if victim_id:
			living_npcs.remove(victim_id)
		
		# players location
		npcs_enter = []
		npcs_exit = []
		
		for npc in living_npcs:
			do_move = random.choice([True, False])
			if do_move:
				destination = random.choice(sql.get_npc_possible_directions(npc))
				
				if destination == player.location:
					npcs_enter.append((npc, sql.get_npc_location(npc)))
				
				elif sql.get_npc_location(npc) == player.location:
					npcs_exit.append((npc, destination))	
				
				sql.move_npc(npc, destination)
		

		npcs_enter_message = npc_move_message(npcs_enter, 'enter')
		npcs_exit_message = npc_move_message(npcs_exit, 'exit')
		
		## MOVE THESE SOMEWHERE ELSE
		DEBUG (npcs_enter_message)
		DEBUG (npcs_exit_message)
		
		# Execute -------------------------------------------------------------
		if victim_id and current_murderer_id:
			sql.murder(victim_id, current_murderer_id)
			
		# Clues ---------------------------------------------------------------
		if victim_id:
		#	DEBUG ("{0} was killed".format(sql.npc_name_from_id(victim_id)))
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
					
					# DEBUG("Added clue {0} to {1}.".format(sql.detail_name_from_id(clue), sql.npc_name_from_id(witness_id)))
		#		DEBUG ("Yes witnesses")
		#	else:
		#		DEBUG ("No witnesses")
				
		#Reset
		victim_id = None
	
	# PLAYER ACTION SECTION ===================================================
	# Receive and process input
	# Get input, lower and split it
	# Look for two part words
	# Look for synonyms, and swap
	raw_command = input (">> ").lower().split()
	if len(raw_command) == 0:
		continue
	
	# instant terminate
	if raw_command[0] == 'exit':
		playing = False
		continue
	
	if raw_command [0] == 'show' and raw_command[1] == 'murderers':
		murderers = sql.get_active_murderers()
		for item in murderers:
			print ("\t{0}".format(formatter.name(sql.npc_name_from_id(item))))
		print ("\n\n")
		continue
	
	# Actual meaningful words
	verb = None
	target1 = None
	preposition = None
	target2 = None

	# For guessing names
	first_filled_npc = None
	second_filled_npc = None
	bad_name_message = None
	
	word_range = len(raw_command)
	index = 0
	while index < word_range:
		command_word = raw_command[index]
		next_word = None
		
		# Don't look last word, since it can't be first of two part word ------
		if index < word_range - 1:
			next_word = raw_command [index + 1]
			parts = sql.get_two_part_words(command_word)
			if parts != None and next_word in parts:
				command_word = "{0} {1}".format(command_word, next_word)
				index += 1


		# Check for synonyms --------------------------------------------------
		command_word = sql.get_word_from_synonym(command_word)
		
		# Check for full name after synonyms ----------------------------------
		npcs_in_room = sql.all_npc_names_in_room(player.location)
		
		if command_word in first_names and next_word == sql.get_last_name(command_word):
			command_word = command_word, next_word
			index += 1
			
			if not first_filled_npc:
				first_filled_npc = sql.npc_id_from_name(command_word)
			elif not second_filled_npc:
				second_filled_npc = sql.npc_id_from_name(command_word)

		else:
			first_name = False
			last_name = False
	
			if not first_filled_npc:
				context = ['room', player.location]
			elif not second_filled_npc and verb == 'ask': 
				context = ['clue', first_filled_npc]
			elif not second_filled_npc and verb == 'blame':
				context = ['murder', first_filled_npc]
			else:
				context = None
			
			if command_word in first_names:
				first_name = command_word
				last_name = find_other_name(context, first_name)
				
			elif command_word in last_names:				
				last_name = command_word
				first_name = find_other_name(context, last_name)

			if first_name and last_name:
				command_word = first_name, last_name
				
				if not first_filled_npc:
					first_filled_npc = sql.npc_id_from_name(command_word)
				elif not second_filled_npc:
					second_filled_npc = sql.npc_id_from_name(command_word)
					
				#DEBUG ("cmd test: " + str(command_word))
				
			elif first_name:
				bad_name_message = "Which {0} do you mean?".format(first_name.title())
				break
			elif last_name:
				bad_name_message = "You have to be more specific. Which {0} do you mean?".format(last_name.title())
				break
			
			## this seems to be done, although it have never occured due to context sensitive name guesser
			## MESSAGE HERE TO TELL PLAYER TO BE MORE SPECIFIC ABOUT NAME
		# ---------------------------------------------------------------------
		
		#command.append (command_word)
		
		if verb is None:
			if command_word in verbs:
				verb = command_word
				
			elif command_word in directions or command_word in specials:
				target1 = command_word
		
		elif preposition is None:
			
			if command_word in targets and target1 is None:
				target1 = command_word
				
			elif command_word in prepositions:
				preposition = command_word
					
		elif target2 is None:
			
			if command_word in targets:
				target2 = command_word
		
		index += 1
	# End of command parsing loop ---------------------------------------------
	
	# Check if bad name found -------------------------------------------------
	if bad_name_message:
		fprint(bad_name_message)
		continue
				
	# Check if player entered only direction ----------------------------------
	if target1 in long_directions:
		target1 = sql.short_direction(target1)
	
	if verb is None:
		if target1 in directions:
			verb = 'move'
			target2 = target1
			target1 = None
			
	if target1 == 'notes' and (verb is None or verb == 'look'):
		verb = 'look'
		target1 = None
		preposition = 'at'
		target2 = 'notes'
			
	# DEBUG ("{0} {1} {2} {3}".format(verb, target1, preposition, target2))
	
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
				movement = move.move(target2)
				fprint (movement[1])
				if movement [0]:
					fprint(look.look(sql.room_name_from_id(player.location)))
					use_action_point = True
				
			elif super == 2: # LOOK
				if sub == 0:
					fprint(look.look(target2))
				
				elif sub == 1:
					fprint(look.look_around())
		
			elif super == 3: # ASK
				fprint(ask.ask(target1, target2))
				use_action_point = True
			
			elif super == 4: # BLAME
				fprint(blame.blame(target1, target2))
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