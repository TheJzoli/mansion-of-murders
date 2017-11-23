import random

import move
import look 
import sql

## UNIVERSAL FUNCTIONS
def fprint (text):
	print (text)
	
 
## VOCABULARY
Move = ['move', 'walk', 'go']
Look = ['look']
Directions = []
prepositions = ['to', 'at']
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
	if (commands [0] in Look):
		fprint (look.show_room (current_room))                                                                                         

#	elif (commands [0] in Ask)
		
#	elif (commands [0] in Blame)
	
	elif (commands [0] in exit_words):
		playing = False
		
	else:
		invalid_command = True	
	
	if (invalid_command):
		fprint("That makes no sense!")

fprint ("You leave the mansion, and none of the murders are your concern anymore. Good riddance!")