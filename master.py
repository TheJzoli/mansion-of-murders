import common
from common import *

import random
	
import sql
import move
import look
import ask
import blame


from os import system

win_width = 92
win_height = 50
buffer_height = 9999

# These set window size and buffer size
system('mode con: cols={0} lines={1}'.format(win_width, win_height))
system('powershell -command "&{$H=get-host;$W=$H.ui.rawui;$B=$W.buffersize;$B.width=' + str(win_width) + ';$B.height=' + str(buffer_height) + ';$W.buffersize=$B;}')


# This sets background and font colours, and fills console with color
print(default_colour)
system('cls')

colours = True
cmd_prompt = "@c>>" + cmd_colour

del system


'''
# Lets just keep this until above shows its thrustworthiness
try:
	from colorama import init
	init()

	
	# set and fill screen with default colour
	print(default_colour)
	print('\x1b[2J')
	
	cmd_prompt += cmd_colour
	
	colours = True
except:

	# Clear screen
	import os
	os.system('cls')
	del os

	print("Colours disabled.\n")
	colours = False
'''	


# This controls text output beyond vanilla print
import re
pattern = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
left_offset = 5
row_length = 80 + left_offset
tab_length = 8
def fprint (text):
	
	if text[-1] == '\n':
		text = text[:-1]
	
	# Add highlight
	text = text.replace('@H', cmd_colour)
	text = text.replace('@E', default_colour)
	
	text = text.replace('\t', tab_length * ' ')
	
	if not colours:
		text = pattern.sub('', text)

	lines = text.split (sep = "\n")

	for i in range (len(lines)):
		line_offset = 0
		words = lines[i].split(" ")
		end = "\n"
		
		# Special commands used with @
		# @i: line is not split, and will retain its whitespace and indent
		# @s: for npcs speaking, indents speaking nicely
		# @c: like @i, but also ending without newline, used for prompting input from player
		
		if len(lines[i]) >= 2 and lines[i][0] == "@":
			other = lines [i][1]
			if other == 'i':
				words = [lines[i][2:]]
				
			elif other == 's':
				words[0] = words[0][2:]
				line_offset = len(words[0]) + 1 + len(words[1]) + 1
				
			elif other == 'c':
				words = [lines[i][2:]]
				end = ""
				
		line = left_offset * " "
		used = 0
		
		for j in range(len(words)):
			word = words [j]
			
			# compute length without ansi sequences
			length = len(pattern.sub('', word))
			if length > 0:
				if used + length < row_length:
					line += word + " "
					used += length + 1
				else:
					#line += (row_length - used) * " "
					line += "\n" + (left_offset + line_offset) * " " + word + " "
					used = line_offset + length + 1
					
			# if word only has color info
			elif pattern.match(word):
				line = word

		#line += (row_length - used) * " "
		lines [i] = (line, end)
	
	for item in lines:
		if len (item[0]) > 0:
			print(item[0], end = item[1])
			
# end fprint ------------------------------------------------------------------

	
def print_all(messages):
	for item in messages:
		fprint (item)
		print()



	
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
npcs = sql.all_npcs()

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
	if moving_npcs == []:
		return None
		
	move_message = ""
	
	if action == 'enter':
		action_str = 'entered'
		preposition = ' from'
	elif action == 'exit':
		action_str = 'left'
		preposition = 'to'
	
	current_room = sql.room_name_from_id(player.location)
	for item in moving_npcs:
		name = format_npc(sql.npc_name_from_id(item[0]))
		other_room = sql.room_name_from_id(item[1])
		move_message += "{0} has {1} the {2} {3} the {4}.\n".format(
														name,
														action_str,
														current_room,
														preposition,
														other_room
														)
	
	return move_message [:-1]



## INTRO ======================================================================

title = (
		"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
		"      __     __      __      __    __    ______    __    _____    __    __      \n"
		"     |  \   /  |    /  \    |  \  |  |  /   _  \  |  |  /  _  \  |  \  |  |     \n"
		"     |   \_/   |   / /\ \   |   \ |  |  \  \  \_\ |  | |  | |  | |   \ |  |     \n"
		"     |         |  / /__\ \  |    \|  |    \  \    |  | |  | |  | |    \|  |     \n"
		"     |  |\_/|  | /   __   \ |  |\    |  _   \  \  |  | |  | |  | |  |\    |     \n"
		"     |  |   |  | |  |  |  | |  | \   | \ \__/   | |  | |  |_|  | |  | \   |     \n"
		"     |__|   |__| |__|  |__| |__|  \__|  \______/  |__|  \_____/  |__|  \__|     \n"
		"                               _____    ______                                  \n"
		"                              /  _  \  |   ___|                                 \n"
		"                             |  | |  | |  |__                                   \n"
		"                             |  | |  | |   __|                                  \n"
		"                             |  | |  | |  |                                     \n"
		"                             |  |_|  | |  |                                     \n"
		"                              \_____/  |__|                                     \n"
		"      __     __   __    __   ______    _____    ______   _____     ______       \n"
		"     |  \   /  | |  |  |  | |   _  \  |  __ \  |   ___| |   _  \  /   _  \      \n"
		"     |   \_/   | |  |  |  | |  |_|  | | |  \ | |  |__   |  |_|  | \  \  \_\     \n"
		"     |         | |  |  |  | |      /  | |  | | |   __|  |      /    \  \        \n"
		"     |  |\_/|  | |  |  |  | |  |\ \   | |  | | |  |     |  |\ \   _   \  \      \n"
		"     |  |   |  | \  \__/  / |  | \ \  | |__/ | |  |___  |  | \ \ \ \__/   |     \n"
		"     |__|   |__|  \______/  |__|  \_\ |_____/  |______| |__|  \_\ \______/      \n"
		"                                                                                \n"
		"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
		)


title = '\n'.join(list(map(lambda x: left_offset * " " + x, title.split(sep = '\n'))))


introduction = (
				"Someone has been killed in the {0}ENTRANCE{1}. "
				"You should {0}MOVE{1} there, and begin to {0}ASK people ABOUT the poor thing{1}. "
				"Once you know the culprit you can {0}BLAME them FOR KILLING the victim{1}. "
				"You can always {0}LOOK AROUND{1} or {0}LOOK AT people{1}, or view your {0}NOTES{1}."
				"\n For help with the commands, type 'help'."
				).format(cmd_colour, default_colour)

introduction = (
				"Welcome to the Mansion of Murders. You've been invited to a ball, at an old English manor well outside the town. "
				"But you're not going there to party, no sir, you're actually a private investigator and "
				"you're working based on a tip you received from no other than the host of the said ball. "
				"He suspects that some of the guest may have hostile intents...\n"
				
				"As soon as you arrive to the mansion murders start to take place and you must act fast. "
				"Using the clues provided by the people who saw the murder, you must identify the murderers "
				"and catch them before it's too late and the party turns into a bloodbath.\n"
				
				"Move around the mansion, ask about the murders, examine the people around you "
				"and when you think you're sure you've identified the correct murderer you can accuse them, "
				"but be careful who you blame because the real murderers may escape.\n"
				)
				
				
				#"@i'move to <room name>'				Moving to another room.\n"
instructions =	("You have three actions in your turn. You can use your actions to following operations:\n"
				 + "@i{0:40} {1}.\n".format("'@HMOVE TO@E <room name>'",'Moving to another room')
				 + "@i{0:40} {1}.\n".format("'@HMOVE@E <direction	>'",'Moving to another room')
				 + "@i{0:40} {1}.\n".format("'@HASK@E <person> @HABOUT@E <dead person>'",'Asking about murders')
				 + "@i{0:40} {1}.\n".format("'@HBLAME@E <person> @HFOR KILLING@E <dead person>'",'Blaming possible murderers')
				 + "\nIn addition, you have following free operations, that don't use up your actions:\n"
				 + "@i{0:40} {1}.\n".format("'@HLOOK AROUND@E', '@HLOOK AT@E <room name>'",'Looking at your surroundings')
				 + "@i{0:40} {1}.\n".format("'@HLOOK AT@E <person>'", 'Looking at a person')
				 + "@i{0:40} {1}.\n".format("'@HLOOK AT NOTES@E'", 'Looking at your notes')
				 + "@i{0:40} {1}.\n".format("'@HASK ABOUT@E <room name>'", 'Finding a way to a room')
				 + "@i{0:40} {1}.\n".format("'@HHELP@E'", 'Getting help')
				 )

print()				
print (title)
fprint ("Press ENTER to start game")
input()

#fprint(introduction)
print_all ([introduction, instructions])

## ============================================================================
##                            GAME LOOP
## ============================================================================
fprint("...")
print()

# First murder must happen in entrance, so that player finds it early
# It is enough to move the first murderer there, because all npcs are dealt evenly across rooms
first_murderer = sql.query_single("SELECT MIN(mapped_id) FROM mapped_npc WHERE state = 'murdering';")
sql.move_npc(first_murderer, sql.room_id_from_name('entrance'))

# Still start murderer index from 0
current_murderer_id = 0

# Start at full used actions, so that npcs will move on first turn
player_actions = 3
player_actions_used = player_actions

playing = True
first_turn = True
delayed_messages = []

round = 0

while (playing):
	game_turn = False
	if player_actions_used == player_actions:
		player_actions_used = 0
		game_turn = True
	
	if first_turn:
		status_message = ""
	else:
		status_message = "Player actions left: @H{0}@E\n".format(player_actions - player_actions_used)
	
	if delayed_messages:
		DEBUG("delayed messages: " + str(delayed_messages))
	
	messages = []
	for i in range(len(delayed_messages)):
		if delayed_messages[i][1]:
			messages.append(delayed_messages[i][0])
			del delayed_messages[i]
			i -= 1

	# GAME ROUND ACTION =======================================================
	if game_turn:
		
		round += 1
		status_message = "Games turn! Round @H{0}@E {1}\n{2}".format (round, (win_width - (37 if round >= 10 else 36)) * '-', status_message)
		
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
		
		if possible_targets:
			victim_id = random.choice(possible_targets)
			
			murderer_location = sql.get_npc_location (current_murderer_id)
			victim_location = sql.get_npc_location(victim_id)
			sql.move_npc(current_murderer_id, victim_location)
		
			if victim_location != murderer_location:
				DEBUG ("Murderer {0} moved from {1} to {2} to kill {3}!".format(sql.npc_name_from_id(current_murderer_id), sql.room_name_from_id(murderer_location), sql.room_name_from_id(victim_location), sql.npc_name_from_id(victim_id)))
			else:
				DEBUG ("Murderer {0} killed {1} in {2}!".format(sql.npc_name_from_id(current_murderer_id), sql.npc_name_from_id(victim_id), sql.room_name_from_id(victim_location)))

		else:
			DEBUG("No targets left for remaining killer {0}.".format(sql.npc_name_from_id(current_murderer_id)))
			
			
		# Npcs move -----------------------------------------------------------
		# From and to player's location
		npcs_enter = []
		npcs_exit = []
		
		for npc in sql.get_living_npcs():
			if npc in [current_murderer_id, victim_id]:
				do_move = False
			elif npc in murderers:
				do_move = True
			else:
				do_move = random.choice([True, False])
				
			if do_move:
				location = sql.get_npc_location(npc)
				destination = random.choice(sql.get_adjacent_rooms(location))
				
				if destination == player.location:
					npcs_enter.append((npc, location))
				
				elif location == player.location:
					npcs_exit.append((npc, destination))	
				
				sql.move_npc(npc, destination)

		#if not round == 0:
		if not first_turn:
			if npcs_enter:
				messages.append (npc_move_message(npcs_enter, 'enter'))
			if npcs_exit:
				messages.append (npc_move_message(npcs_exit, 'exit'))
			
		# Execute murder and deal clues ---------------------------------------
		if victim_id and current_murderer_id:
			sql.murder(victim_id, current_murderer_id)
			
			clues = sql.get_details(current_murderer_id);
			shuffle(clues)
			
			witnesses = sql.live_npcsid_in_room(victim_location)
			safe_remove(current_murderer_id, witnesses)
			
			if victim_location == player.location:
				witnesses.append('player')
				sql.add_player_clue(victim_id, None)
			
			player_clues = []
			
			shuffle(witnesses)			
			if len(witnesses) > 0:
				for i in range (5):
					clue = clues [i]
					witness_id = witnesses [i % len(witnesses)]
					if witness_id == 'player':
						player_clues.append(clue)
						sql.add_player_clue(victim_id, clue)
					else:						
						sql.add_clue (victim_id, witness_id, clue)
						
						
			if victim_location == player.location:
				victim_name = format_npc(sql.npc_name_from_id(victim_id))
				if player_clues:
					murder_message = (
									"Right in front of your eyes, someone killed {0}!"
									" @HYou saw that the killer had {1}@E."
									).format(victim_name, format_list(player_clues, sql.detail_name_from_id))
					
					
				else:
					murder_message = "{0} collapses on ground, dead. @HBut who is the killer!@E".format(victim_name)
				messages.append (murder_message)
			
			else:		
				npcs_in_players_room = lambda: len(sql.live_npcsid_in_room(player.location)) > 0
				room_name = format_room(sql.room_name_from_id(victim_location))
				murder_message = "You hear people talking about @Hsomeone being killed in the {0}@E.".format(room_name)
				if npcs_in_players_room ():
					messages.append (murder_message)
				else:
					delayed_messages.append((murder_message, npcs_in_players_room))
			
		
		#Reset
		victim_id = None
	
	messages.insert(0, status_message)
	
	# NPC Printing =========================================================		
	print_all(messages)
	messages = []
	# PLAYER ACTION SECTION ===================================================
	# Receive and process input
	# Get input, lower and split it
	# Look for two part words
	# Look for synonyms, and swap
	if first_turn:
		raw_command = ['look']
		first_turn = False

	else:
		fprint (cmd_prompt)
		raw_command = input ().lower().split()
		#print(default_colour, end = "")
		fprint("@c" + default_colour)
		
	if len(raw_command) == 0:
		continue
	
	# Lazy cheat commands
	cheat = False
	if raw_command[0] == 'exit':
		playing = False
		end_state = None
		continue
	
	if len(raw_command) > 4 and raw_command[0] == 'move' and raw_command[1] in first_names and raw_command[2] in last_names and raw_command[3] == 'to':
		npc = ((raw_command[1], raw_command[2]))
		npc_id = sql.npc_id_from_name(npc)
		if len(raw_command) >= 6:
			room_name = "{0} {1}".format(raw_command[4], raw_command[5])
			if room_name in rooms:
				print_all(["Moved {0} to the {1}.".format(format_npc(npc), format_room(room_name))])
				sql.move_npc(npc_id, sql.room_id_from_name(room_name))
				continue
		elif raw_command[4] in rooms:
			print_all(["Moved {0} to the {1}.".format(format_npc(npc), format_room(raw_command[4]))])
			sql.move_npc(npc_id, sql.room_id_from_name(room_name))
			continue
			
	elif raw_command[0] == 'cheat':
		cheat = True
		raw_command = raw_command [1:]
	
	elif raw_command [0] == 'show':
		if raw_command[1] == 'murderers':
			murderers = sql.get_active_murderers()
			message = "Murderers:"
			for item in murderers:
				message += ("\n@i\t{0:30}{1}".format(
											format_npc(sql.npc_name_from_id(item)),
											sql.room_name_from_id(sql.get_npc_location(item))
											))
			print_all ([message])
			continue
		
		elif raw_command[1] == 'quests':
			npcs = sorted(sql.all_npcs(), key = lambda x: sql.npc_id_from_name(x))
			printout = "Quests:"
			for item in npcs:
				mapped_id = sql.npc_id_from_name(item)
				dead = "Dead" if item not in sql.live_npcs() else ""
				printout += ("\n@i\t{0:2} {1:30}{2:18} {3}".format(
												mapped_id,
												format_npc(item),
												format_room(sql.room_name_from_id(sql.get_npc_location(mapped_id))),
												dead
												))
			print_all ([printout])
			continue
			
		
	elif raw_command [0] == 'teleport':
		if len(raw_command) >= 3:
			room_name = "{0} {1}".format(raw_command[1], raw_command[2])
			if room_name in rooms:
				player.location = sql.room_id_from_name(room_name)
				print_all (["Teleported to {0}.".format(room_name)])
				continue
				
		elif raw_command [1] in rooms:
			player.location = sql.room_id_from_name(raw_command[1])
			print_all (["Teleported to {0}.".format(raw_command[1])])
			continue
	
	elif raw_command [0] == 'help':
		print_all([instructions])
		continue
	
	
	elif raw_command[0] == 'rooms':
		sorted_rooms = sorted(rooms, key = lambda x: sql.room_id_from_name(x))
		rooms_str = ""
		for item in sorted_rooms:
			rooms_str += ("{0:2} {1}\n".format (sql.room_id_from_name(item),item))
		print_all([rooms_str])
		
	elif raw_command [0] == 'ragequit' or raw_command[0] == 'rage' and raw_command[1] == 'quit':
		end_state = 'ragequit'
		playing = False
		break
		
	# Actual meaningful words
	verb = None
	target1 = None
	preposition = None
	target2 = None

	# For guessing names
	first_filled_npc = None
	second_filled_npc = None
	bad_name_message = None
	
	#DEBUG_command = []
	
	word_range = len(raw_command)
	index = 0
	while index < word_range:
		command_word = raw_command[index]
		next_word = None
		
		
		# Don't look last word, since it can't be first of two part word ------
		if index < word_range - 1:
			next_word = raw_command [index + 1]
			
			#DEBUG ((index, command_word, next_word, sql.get_last_names(command_word)))
			
			
			parts = sql.get_two_part_words(command_word)
			if parts != None and next_word in parts:
				command_word = "{0} {1}".format(command_word, next_word)
				index += 1


		# Check for synonyms --------------------------------------------------
		command_word = sql.get_word_from_synonym(command_word)
		
		# Check for full name after synonyms ----------------------------------
		npcs_in_room = sql.npcs_in_room(player.location)
		
		if command_word in first_names and next_word in sql.get_last_names(command_word):
			command_word = command_word, next_word
			index += 1
			
			if not first_filled_npc:
				first_filled_npc = sql.npc_id_from_name(command_word)
			elif not second_filled_npc:
				second_filled_npc = sql.npc_id_from_name(command_word)

			if bad_name_message:
				DEBUG(("bad name message", bad_name_message))
				
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
			
			
			elif first_name:
				DEBUG("create bad name message")
				bad_name_message = "Which {0} do you mean?".format(first_name.title())
				break
			elif last_name:
				DEBUG("create bad name message")
				bad_name_message = "You have to be more specific. Which {0} do you mean?".format(last_name.title())
				break
			
			## this has some problems, but they are hard to recreate
			## MESSAGE HERE TO TELL PLAYER TO BE MORE SPECIFIC ABOUT NAME
		# ---------------------------------------------------------------------
		
		#DEBUG_command.append (command_word)
		
		if verb is None:
			if sql.in_all_verbs(command_word):
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
		#DEBUG("Standard add index: " + str(index))
	# End of command parsing loop ---------------------------------------------
	
	#DEBUG(DEBUG_command)
	
	# Check if bad name found -------------------------------------------------
	if bad_name_message:
		print_all([bad_name_message])
		continue
				
	# Some handhelding with command typ(o)ing ------------------------------------
	if target1 in long_directions:
		target1 = sql.short_direction(target1)
	
	if target1 in directions and (verb is None or verb == 'move'):
		verb = 'move'
		target2 = target1
		target1 = None
			
	if target1 == 'notes' and (verb is None or verb == 'look'):
		verb = 'look'
		target1 = None
		preposition = 'at'
		target2 = 'notes'
	
	if verb == 'look' and target1:
		target2 = target1
		target1 = None
		preposition = 'at'

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
				messages.append(movement[1])
				if movement [0]:
					messages.append(look.look(sql.room_name_from_id(player.location)))
					use_action_point = True
				
			elif super == 2: # LOOK
				if sub == 0:
					messages.append(look.look(target2))
				
				elif sub == 1:
					messages.append(look.look_around())
		
			elif super == 3: # ASK
				if sub == 0:
					asking = ask.ask(target1, target2)
					#messages.append(ask.ask(target1, target2))
					messages.append(asking[1])
					use_action_point = asking [0]
				
				elif sub == 1:
					messages.append(ask.ask_other(target1, target2))
				
				else:
					messages.append("What do you want to ask?")
				
			elif super == 4: # BLAME
				messages.append(blame.blame(target1, target2))
				use_action_point = True
			
			elif super == 9: # WAIT
				messages.append("Some time passes.")
				use_action_point = True
				
			if use_action_point and not cheat:
				cheat = False
				player_actions_used += 1
		else:
			messages.append("You cannot do that.")
			
	else:
		messages.append("There was no verb, what do you want to do?")
			
			
	# Player Printing =========================================================
	if not messages:
		DEBUG("No messages")
	print_all(messages)
	
	# Check for end condition =================================================
	# no murderers left
	if not sql.get_active_murderers ():
		DEBUG ("Game Finished")
		playing = False
		end_state = 'out of murderers'
		
	# last murderer kills you
	elif len (sql.get_living_npcs()) == 1:
		DEBUG ("Game Over")
		playing = False
		end_state = 'one murderer left'
	
## END GAME LOOP	

points_for_survivor = 10
points_for_solved = 5
points_for_unsolved = 0
	
points = 0

if end_state == 'out of murderers':
	fprint ("You've gotten rid of all the killers. But at what price! {0} people died today.".format (sql.query_single("SELECT COUNT(*) FROM murder")))
	murders = sql.column_as_list(sql.run_query("SELECT state FROM murder INNER JOIN mapped_npc ON mapped_id = murderer;"), 0)

	for item in murders:
		if item == 'arrested':
			points += points_for_solved
		elif item == 'escaped':
			points += points_for_unsolved

	points += (len(npcs) - len(murders)) * points_for_survivor

	max_points = len(npcs) * points_for_survivor - int(len(npcs) / 10) * points_for_solved
	fprint("You got {0} points of {1}.".format(points, max_points))
	
elif end_state == 'one murderer left':
	last_murderer = sql.get_active_murderers()[0]
	formatted_name = format_npc(sql.npc_name_from_id(last_murderer))
	fprint(
			"Just as you thought you got all of them, "
			"{0} proves you wrong by cutting your throat!"
			"\n\n You get no points.".format(formatted_name)
			)

elif end_state == 'ragequit':

	fore = ['\x1b[30m', '\x1b[34m', '\x1b[36m', '\x1b[32m', '\x1b[90m', '\x1b[94m',
	'\x1b[96m', '\x1b[92m', '\x1b[95m', '\x1b[91m', '\x1b[97m', '\x1b[93m',
	'\x1b[35m', '\x1b[31m', '\x1b[39m', '\x1b[37m', '\x1b[33m']

	back = ['\x1b[40m', '\x1b[44m', '\x1b[46m', '\x1b[42m', '\x1b[100m', '\x1b[104m',
	'\x1b[106m', '\x1b[102m', '\x1b[105m', '\x1b[101m', '\x1b[107m', '\x1b[103m',
	'\x1b[45m', '\x1b[41m', '\x1b[49m', '\x1b[47m', '\x1b[43m']

	width = win_width
	height = 30

	from string import punctuation
	field = ""
	for i in range(height):
		for j in range(width):
			color = random.choice ([default_colour, random.choice(fore) + random.choice(back)])
			field += color + random.choice([" ", random.choice(punctuation)])
			
			'''
			f = random.choice (fore)
			b = random.choice (back)
			c = random.choice (punctuation)
			
			
			field += f + b + c
			'''
	print (field + '\x1b[0m')
	print("\n t£ermina1      \n br¤ke                  sdviqk¤%¤%&\n\n bye...")

sql.end()

input ("Press ENTER to exit game.")