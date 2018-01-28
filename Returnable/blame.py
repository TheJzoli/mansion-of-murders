import sql
from common import *

def murder_solved(id_m):
	query = "SELECT state FROM mapped_npc WHERE mapped_id = '{0}';".format(id_m)
	result = sql.query_single(query)
	if(result == 'arrested'):
		message = "You've already caught them."
	elif(result == 'escaped'):
		message = "You're too late, the murderer has already escaped."
	else:
		query = "UPDATE mapped_npc SET state = 'arrested' WHERE mapped_id = '{0}';".format(id_m)
		sql.run_update(query)
		message = "Congratulations you solved a murder and the murderer will be arrested!"
	return message
	
def blamed_location(id_m):
	query = "SELECT location FROM mapped_npc WHERE mapped_id = '{0}';".format(id_m)
	message = sql.query_single(query)
	return message

def escaper(correct_murderer):
	query = "UPDATE mapped_npc SET state = 'escaped' WHERE mapped_id = '{0}';".format(correct_murderer)
	sql.run_update(query)
	message = "Oh no one of the murderers has escaped!"
	return message

	
def blame(murderer,victim):

	
	DEBUG("Blame")
	message = ""
	
	id_m = sql.npc_id_from_name(murderer)
	id_v = sql.npc_id_from_name(victim)
	m_location = blamed_location(id_m)
	
	if m_location == player.location:
	
		query = "SELECT murderer FROM murder WHERE victim = {0};".format(id_v)
		right_murderer = sql.query_single(query)
	
		if right_murderer:
			if right_murderer == id_m:
				message = murder_solved(id_m)
			else:
				query = (
						"select player_clue.detail "
						"from player_clue " 
						"inner join npc_detail on player_clue.detail = npc_detail.detail " 
						"inner join mapped_npc on npc_detail.npc = mapped_npc.npc " 
						"and mapped_npc.mapped_id in ("
							"select murderer "
							"from murder where victim = {0}"
						");"
						).format(id_v)
			
				details = sql.column_as_list(sql.run_query(query),0)
			
				if len(details) < 3:
					message = "They didn't kill that person!"
				else:
					message = escaper(right_murderer)
		else:
			message = "They ain't even dead yet!"
	else:
		message = "You can't blame them, they're not here."
	return message