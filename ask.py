import sql

def ask(witness, victim):
	message = ""
	if witness in sql.live_npcs_in_room(player.location):
		if victim in sql.dead_npcs():
			
	else:
		message = "There is no one called {0} in this room to whom you could talk to.".format(witness)
	
	
	
	return message
#print("Ask {0} about {1}'s killer".format(witness, victim))