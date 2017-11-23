import sql

## GAME LOOP
playing = True
while (playing):
	
	command = input (">>").lower().split()
	
	verb = None
	preposition = None
	target = None
	
	for word in command:
		if (word in sql.get_verbs and verb == None):
			verb = word
		
		if (word in sql.get_prepositions and preposition == None):
			preposition = word
	
	if (command [0] == 'quit'):
		playing = False
	