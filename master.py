import random

## IMPORT COMPONENTS
import move
import look 
import ask
import sql

## UNIVERSAL FUNCTIONS
def fprint (text):
	print (text)
	
 
## VOCABULARY
Move = ['move', 'walk', 'go']
Look = ['look', 'eye', 'glance', 'glimpse', 'peek', 'view', 'gander', 'gaze', 'inspect', 'leer', 'observe', 'watch']
Ask = ['ask', 'inquire', 'question']

Murder = ['murder', 'case']

Directions = []
prepositions = ['to', 'at', 'about']
exit_words = ['exit', 'quit']

## PLAYER LOCATION
current_room = 1

playing = True
while playing:
    
	live_npcs_in_room = []
	dead_npcs_in_room = []
	live_npcs = []
	dead_npcs = []

	command = input(">>")
	commands = command.lower().split()
	cmd_len = len(commands)
	
	invalid_command = False
	
	
	## MOVE TO ROOMS
	if (commands [0] in Move):
		if (cmd_len > 1):
			if (commands [1] in prepositions and cmd_len > 2):
				if (commands [1] == 'to'):
					move.move (commands [2])
				else:
					invalid_command = True
			else:
				room = commands [1]
		else: #cmd_len == 1
			fprint ("Where do you want to go?")
	
	## LOOK
	elif (commands [0] in Look):
		fprint (look.show_room (current_room))                                                                                         
	
	## ASK
	live_npcs_in_room = ['johnsson', 'petersson', 'kekkonen']
	dead_npcs = ['deadman', 'youngman']
	
	if (commands[0] in Ask):
		if (cmd_len > 1):
			if (commands[1] in live_npcs_in_room):
				if (cmd_len > 2):
					if (commands[2] in prepositions):
						if (commands[2] == 'about'):
							if (cmd_len > 3):
								if (commands[3] in dead_npcs):
									if (cmd_len > 4):
										if (commands[4] in Murder):
											if (cmd_len > 5):
												if (commands[5] == 'case'):
													fprint(ask.ask("dead"))
												else:
													fprint("uuh what?")
											else:
												fprint(ask.ask("dead"))
										else: #They ask about something other than murder
											fprint("Why would you want to ask that?")
									else: #If they ask without adding "murder" to the end
										fprint(ask.ask("dead"))
								else: #An NPC that is not dead
									fprint(ask.ask("alive"))
							else: #If they only "Ask NPC about"
								fprint("About what?")
						else: #They use the wrong preposition
							fprint("Now that doesn't make any sense!")
					else: #They don't use a preposition
						invalid_command = True
				else: #If they only "Ask NPC"
					fprint("Ask what?")
			elif (commands[1] in dead_npcs): #They're a dead NPC
				fprint("Dead men tell no tales...")
			else: #No NPC of that name in room
				fprint("There is no such person here to talk to.")
		else: #If they only "Ask"
			fprint("Who?")
#	elif (commands [0] in Ask)
		
#	elif (commands [0] in Blame)
	
	elif (commands [0] in exit_words):
		playing = False
		
	else:
		invalid_command = True	
	
	if (invalid_command):
		fprint("That makes no sense!")

sql.end()
fprint ("You leave the mansion, and none of the murders are your concern anymore. Good riddance!")