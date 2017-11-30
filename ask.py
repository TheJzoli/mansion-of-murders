import sql

murderer_detail = sql.murderer_detail

def ask(witness, victim):
	message = ""
	if witness in sql.live_npcs_in_room(player.location):
		if victim in sql.dead_npcs():
			if (murderer_detail == ""):
				message = "Wait? " + victim + " has been murdered? How horrible! I didn't know!"
			else:
				message = "{0}: How horrible... If I remember correctly, the murderer had a {1}.".format(witness, murderer_detail)
		elif (victim in sql.live_npcs):
			message = "{0}: {1}? What are you talking about? They haven't been murdered.".format(witness, victim)
		else:
			message = "{0}: {1}? Never heard of anyone called that before.".format(witness, victim)
	else:
		message = "There is no one called {0} in this room to whom you could talk to.".format(witness)
	
	
	
	return message
#print("Ask {0} about {1}'s killer".format(witness, victim))


''' 
How do I see if the Witness has seen another murder by the Murderer....!!!


Check the id of the MURDERER of the current VICTIM... ----SELECT mapped_id FROM mapped_npc INNER JOIN murder ON mapped_id = murder.murderer WHERE murder.victim = sql.victim_id(victim);----
Search for other VICTIMS(id) with the same MURDERER ---- Done ----
search for WITNESSES who have seen both murders(VICTIMS)
if current WITNESS is one of them ^, make him say	
the earlier VICTIM's name.