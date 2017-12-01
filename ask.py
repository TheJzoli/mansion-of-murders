import sql

#murderer_detail = sql.murderer_detail

def ask(witness, victim):
	message = ""
	if witness in sql.live_npcs_in_room(player.location):
		if victim in sql.dead_npcs():
			details = sql.murderer_detail(witness, victim)
			if (details == None):
				message = "{0}: Wait? {1} has been murdered? How horrible! I didn't know!".format (witness, victim)
			else:
				message = "{0}: How horrible... If I remember correctly, the murderer had a {1}.".format(witness, details)
				if (sql.npc_id_from_name(witness) in sql.witnessed_multiple_murders(victim)):
					message += " Oh and also, the murderer was the same person who murdered "
					all_but = sql.all_but_current_murder_victims(victim)
					for i in all_but:
						message += "{0}".format(sql.npc_name_from_id(i))
						if (i != all_but[-1]):
							message += ", "
							if (len(all_but) >= 2):
								if (i == all_but[-2]):
									message += "and "
					message += "."
		elif (victim in sql.live_npcs()):
			message = "{0}: {1}? What are you talking about? They haven't been murdered.".format(witness, victim)
		else:
			message = "{0}: {1}? Never heard of anyone called that before.".format(witness, victim)
	else:
		message = "There is no one called {0} in this room to whom you could talk to.".format(witness)
	
	
	
	return message
#print("Ask {0} about {1}'s killer".format(witness, victim))


''' 
How do I see if the Witness has seen another murder by the Murderer....!!!


Check the id of the MURDERER of the current VICTIM... ----done----
Search for other VICTIMS(id) with the same MURDERER ---- Done ----
search for WITNESSES who have seen both murders(VICTIMS) ----DONE----
if current WITNESS is one of them ^, make him say	
the earlier VICTIM's name.
'''