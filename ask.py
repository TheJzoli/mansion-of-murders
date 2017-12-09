import sql
import random
from common import *


## Jos murha on ratkennut, niin se keneltä kysytään vois sanoo mikä helpotus tms
## pystyy kysyy ihmisiltä, jotka ei oo samassa huoneessa
## ja jos se tietää muita murhia, niin niihin voisi lisätä ne vihjeet

def ask(witness, victim):
	message = ""
	if witness in sql.live_npcs_in_room(player.location):
		if victim in sql.dead_npcs():
			details = sql.murderer_detail(witness, victim)
			

			if (details == None):
				message = "@s{0}: Wait? {1} has been murdered? How horrible! I didn't know!".format (format_npc(witness), format_npc(victim))
			else:

				for item in details:
					sql.add_player_clue(sql.npc_id_from_name(victim), item)
				
				for i in range (len(details)):
					details[i] = sql.detail_name_from_id(details[i])
				
				message = "@s{0}: How horrible... If I remember correctly, the murderer had {1}.".format(format_npc(witness), details)
				if (sql.npc_id_from_name(witness) in sql.witnessed_multiple_murders(victim)):
					message += " Oh and also, the murderer was the same person who murdered "
					all_but = sql.all_but_current_murder_victims(victim)
					for i in all_but:
						message += "{0}".format(format_npc(sql.npc_name_from_id(i)))
						if (i != all_but[-1]):
							message += ", "
							if (len(all_but) >= 2):
								if (i == all_but[-2]):
									message += "and "
					message += "."
		elif (victim in sql.live_npcs()):
			message = "@s{0}: {1}? What are you talking about? They haven't been murdered.".format(format_npc(witness), format_npc(victim))
		else:
			message = "@s{0}: {1}? Never heard of anyone called that before.".format(format_npc(witness), format_npc(victim))
	else:
		message = "There is no one called {0} in this room to whom you could talk to.".format(format_npc(witness))
	
	return message
#print("Ask {0} about {1}'s killer".format(witness, victim))

def ask_direction(destination_room):
	destination_room_id = sql.room_id_from_name(destination_room)
	
	if destination_room_id == player.location:
		message = "You are already there!"
	
	else:
		path = sql.find_path(player.location, destination_room_id)	
		npcs = sql.live_npcsid_in_room(player.location)
		if len(npcs) > 0:
			name = format_npc(sql.npc_name_from_id(random.choice(npcs)))
			message = "{0} tells you the way:\n".format(name)
			for item in path:
				room_name = format_room(sql.room_name_from_id(item[0]))
				direction = sql.long_direction(item[1])
				message += "@i\t{0:20} {1}\n".format(room_name, direction)
		else:
			room_name = format_room(sql.room_name_from_id(path[0][0]))
			message = "There's no one here to help you, but you feel you should go first to the {0}.".format(room_name)
		
	return message


	
	
	
	
	
	