import sql
import random
from common import *

def ask(witness, victim):
	
	victim_id = sql.npc_id_from_name(victim)
	witness_id = sql.npc_id_from_name(witness)
	murderer_id = sql.get_murderer_id(victim_id)
	
	message = ""
	success = False
	
	#f witness in sql.live_npcs_in_room(player.location):
	if witness in sql.live_npcs() and witness in sql.npcs_in_room(player.location):
		success = True
		if victim in sql.dead_npcs():
			details = sql.murderer_detail(witness, victim)
			
			# Arrested means here that murder is solved
			if (sql.npc_state(murderer_id) == 'arrested'):
				message = "@s{0}: The murderer was caught? Oh thank goodness, what a relief!".format(format_npc(witness))
			
			# This npc has no clue
			elif (details == None):
				message = "@s{0}: Wait? {1} has been murdered? How horrible! I didn't know!".format (format_npc(witness), format_npc(victim))
			
			# NPC happily shares their clues
			else:

				for item in details:
					sql.add_player_clue(sql.npc_id_from_name(victim), item)
	
				detail_names = format_list(details, sql.detail_name_from_id)			
				message = "@s{0}: How horrible... If I remember correctly, the murderer had {1}.".format(format_npc(witness), detail_names)
				
				other_victims = sql.witnessed_victims(witness_id, murderer_id).remove(victim_id)

				if other_victims:
					other_victims = format_list (other_victims, lambda x: format_npc(sql.npc_name_from_id(x)))
					message += " Oh and also, the murderer was the same person who murdered {0}.".format(other_victims)
					
				
		elif victim in sql.live_npcs():
			message = "@s{0}: {1}? What are you talking about? They haven't been murdered.".format(format_npc(witness), format_npc(victim))
		else:
			message = "@s{0}: {1}? Never heard of anyone called that before.".format(format_npc(witness), format_npc(victim))
	
	elif witness in sql.dead_npcs() and witness in sql.npcs_in_room(player.location):
		message = "Death has closed their lips for good."
		
	else:
		message = "There is no one called {0} in this room to whom you could talk to.".format(format_npc(witness))
	
	return (success, message)

def ask_other(target1, target2):
	target = target1 or target2

	if target in sql.get_rooms():
		destination_id = sql.room_id_from_name(target)
	
		if destination_id == player.location:
			message = "You are already there!"
	
		else:
			path = sql.find_path(player.location, destination_id)	
			npcs = sql.live_npcsid_in_room(player.location)
			if len(npcs) > 0:
				name = format_npc(sql.npc_name_from_id(random.choice(npcs)))
				message = "{0} tells you the way:\n".format(name)
				for item in path:
					room_name = format_room(sql.room_name_from_id(item[0]))
					direction = sql.to_long_direction(item[1])
					message += "@i\t{0:20} {1}\n".format(room_name, direction)
			else:
				room_name = format_room(sql.room_name_from_id(path[0][0]))
				message = "There's no one here to help you, but you feel you should go first to the {0}.".format(room_name)
				
	elif target in sql.all_npcs():
		
		target_alive = target in sql.live_npcs()
		target_present = target in sql.npcs_in_room(player.location)
		player_has_clue = sql.npc_id_from_name(target) in sql.column_as_list(sql.run_query("SELECT DISTINCT victim FROM player_clue;"), 0)

		if target1:
			if target_alive and target_present:
				message = "Who do you want to ask about from {0}?".format(format_npc(target))
				
			elif not target_present and (target_alive or not player_has_clue):
				message = "{0} is not here. Go ask somebody else.".format(format_npc(target))
			
			elif not target_alive and target_present:
				message = "You see {0} dead on ground. They don't say anything.".format(format_npc(target))
			
			elif not target_alive and not target_present and player_has_clue:
				message = "{0} is not here. As well as not alive.".format(format_npc(target))
		
		else:	
			message = "Whom do you want to ask about {0}?".format(format_npc(target))
	
	elif target in sql.get_all_directions():
	
		target = sql.to_long_direction(target)
		if target1:
			if  target == 'up':
				if sql.room_name_from_id(player.location) in ['front yard', 'back yard']:
					target = 'sky'
				else:
					target = 'ceiling'
			elif target == 'down':
				target = 'floor'
			message = "{0} doesn't tell you anything.".format(target.title())
		else:
			message = "But... Why? Don't do that."
	
	elif target in sql.get_specials():
		if target == 'notes':
			message = "You keep notes of clues you have collected. Type 'memo' or 'notes' to view them."
	
	else:
		message == "This is secret development question. You shold not ever again ask it."
	
	return message


	
	
	
	
	
	