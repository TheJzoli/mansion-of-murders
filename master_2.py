import sql

def fprint (text):
	print (text)

## VOCABULARY
verbs = sql.get_verbs()
prepositions = sql.get_prepositions()
	
## GAME LOOP
playing = True
while (playing):
	
	command = input (">>").lower().split()
	
	print (command)
	
	verb = None
	preposition = None
	target = None
	
	for word in command:
	
		if (verb == None and word in verbs):
			verb = word
			continue
		
		if (preposition == None and word in prepositions):
			preposition = word
			continue
	
	fprint ("{0} {1}".format(verb, preposition))
	
	if (command [0] == 'quit'):
		playing = False


