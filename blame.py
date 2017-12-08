import sql
from debug import DEBUG as DEBUG

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
	
	return message





'''
import sql

def DEBUG (message):
	print ("BLAME DEBUG: " + str(message))

def get_murder(id_m,id_v):
    #query = "SELECT murderer FROM murder WHERE murderer = '" + id_m + "' AND victim = '" + id_v + "';"
	query = "SELECT murderer FROM murder WHERE murderer = '{0}' AND victim = '{1}';". format(id_m, id_v)
	return sql.column_as_list(sql.run_query(query), 0)

def murder_solved(id_m):
	# näitä ei tarvi, solvedia ei oo enää olemassa, vaan pitää kattoo onko murhaaja pidätetty
	# otin siksi myös id_v:n pois
	#query1 = "UPDATE murder SET solved = 1 WHERE murderer = '" + id_m + "' AND victim = '" + id_v + "';"
    #sql.run_query(query1)
	
    #query2 = "UPDATE mapped_npc SET state = 'arrested' WHERE mapped_id = '" + id_m + "';"
	query = "UPDATE mapped_npc SET state = 'arrested' WHERE mapped_id = '{0}';".format(id_m)
	
	# tälle on myös oma funktio :D
	sql.run_update(query)
    #other updates?
	return

def escaper(id_m):
	#query = "UPDATE mapped_npc SET state = 'escaped' WHERE mapped_id = '" + id_m + "';"
	query = "UPDATE mapped_npc SET state = 'escaped' WHERE mapped_id = '{0}';".format(id_m)
	sql.run_query(query)
	return

def victim_id (victim):
	query = (
			"SELECT npc_id FROM murder "
			"INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim "
			"INNER JOIN npc ON npc.npc_id = mapped_npc.npc "
			"WHERE first_name = '{0}' AND last_name = '{1}';"
			).format(victim[0], victim[1])
	return sql.query_single(query)

def murderer_id(murderer):
	query = (
			"SELECT npc_id FROM murder "
			"INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.murderer "
			"INNER JOIN npc ON npc.npc_id = mapped_npc.npc "
			"WHERE first_name = '{0}' AND last_name = '{1}';"
			).format(murderer[0],murderer[1])
	return sql.query_single(query)

	
def blame(murderer,victim):
	message = ""
	id_m = murderer_id(murderer)
	id_v = victim_id(victim)
	murdercount = len(get_murder(id_m,id_v))
	
	# Leon hätäri -------------------------------------------------------------
	id_m = sql.npc_id_from_name(murderer)
	id_v = sql.npc_id_from_name(victim)
	
	query = "SELECT murderer FROM murder WHERE victim = {0};".format(id_v)
	murderer = sql.query_single(query)
	if murderer:
		if murderer == id_m:
			murder_solved(id_m)
			message = "Congratulations you solved a murder and the murderer will be arrested!"
		else:
			message = "They didn't kill that person!"
	else:
		message = "They aren't even dead yet!"
	
	return message
	# Leon hätäri loppu -------------------------------------------------------
	
	if murdercount == 1:
		murder_solved(id_m)
		message = "Congratulations you solved a murder and the murderer will be arrested!"
	else:
		#(false = 0) ei voi tulla aina. while loopin alkuun?
		if false < 3:
			message = "Wrong accusation!"
			false = false + 1
		else:
			message = "Oh no too many false accusations! Now one of the real murderers escaped!"
			escaper(id_m)
			false = 0
	return message


'''