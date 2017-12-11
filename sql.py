import mysql.connector

from common import *

default = "SELECT message FROM error;"

## DATABASE
database = mysql.connector.connect(
	host = 'localhost',
	user = 'dbuser',
	passwd = 'dbpass',
	db = 'mom_game',
	buffered = True)


cursor = database.cursor()
cursor.execute("DELETE FROM player_clue;")
cursor.execute("DELETE FROM clue;")
cursor.execute("DELETE FROM murder;")
cursor.execute("DELETE FROM mapped_npc;")

DEBUG ("Connected to database.")

# Close and reset database
def end ():
	database.rollback()
	database.close()

# Return single column from sql table as array	
def column_as_list (table, column_id):
	column = [] 
	for row in table:
		column.append(row[column_id])
	return column
	
	
	
	
	
## SQL FUNCTIONS --------------------------------------------------------------
def run_query (query):
	cursor = database.cursor()
	cursor.execute (query)
	return cursor.fetchall()
	
def query_single (query):
	result = run_query(query)
	if result:
		return result [0][0]
	else:
		return None

def run_update (update):

	cursor = database.cursor()
	cursor.execute(update)
	
	
	
	
## PARSER FUNCTIONS -----------------------------------------------------------
def get_two_part_words (word):
	query = "SELECT word_2 FROM two_part_words WHERE word_1 = '{0}';".format(word)
	result = run_query (query)
	if result:
		return column_as_list (result, 0)
	else:
		return None

def get_word_from_synonym (word):
	query = "SELECT main_word FROM synonyms WHERE word = '{0}';".format(word)
	result = query_single (query)
	if result == None:
		result = word
	return result
		
def get_verbs():
	query = "SELECT word FROM verb;"
	result = run_query(query)
	return column_as_list (result, 0)

def get_prepositions():
	query = "SELECT word FROM prepositions;"
	result = run_query (query)
	return column_as_list (result, 0)

def get_rooms ():
	query = "SELECT name FROM room;"
	result = run_query (query)
	return column_as_list (result, 0)

def get_npcs ():
	query = "SELECT first_name, last_name FROM npc;"
	return run_query (query)
	
def get_last_names (first_name):
	"""Return last names from database or []"""
	query = "SELECT last_name FROM npc WHERE first_name = '{0}';".format(first_name)
	return column_as_list(run_query(query), 0)
	
# [0] is first name, [1] is last name
def get_npcs_names ():
	query = "SELECT first_name, last_name FROM npc;"
	result = run_query (query)
	return [column_as_list(result, 0), column_as_list (result, 1)]
	
def get_directions ():
	""" Return direction in arrays, [0] is shorts, [1] is longs"""
	query = "SELECT direction_id, name FROM direction;"
	result = run_query (query)
	return [column_as_list(result, 0), column_as_list (result, 1)]

def get_all_directions ():
	"""Fetches direction shorts and longs from database"""
	return get_directions()[0] + get_directions()[1]
	
def get_specials ():
	result = run_query("SELECT word FROM specials;")
	return column_as_list(result, 0)
	
def all_npc_names_in_room(room_id):
	query = (
			"SELECT first_name, last_name "
			"FROM mapped_npc "
			"INNER JOIN npc ON npc_id = mapped_npc.npc "
			"WHERE location = {0}"
			).format(room_id)
	return run_query(query)
	
	
	
## CONVERSIONS ----------------------------------------------------------------
def long_direction (short_direction):
	query = "SELECT name FROM direction WHERE direction_id = '{0}';".format(short_direction)
	return run_query(query)[0][0]

def short_direction(long_direction):
	query = "SELECT direction_id FROM direction WHERE name = '{0}';".format(long_direction)
	return run_query(query)[0][0]
	
def npc_name_from_id (mapped_id):
	query = (
			"SELECT first_name, last_name "
			"FROM mapped_npc "
			"INNER JOIN npc ON npc_id = mapped_npc.npc "
			"WHERE mapped_id = {0};"
			).format(mapped_id)
	return run_query(query)[0]

# This take name as ["first_name","last_name"]
def npc_id_from_name (name):
	query = (
			"SELECT mapped_id "
			"FROM mapped_npc "
			"INNER JOIN npc ON npc_id = mapped_npc.npc "
			"WHERE first_name = '{0}' AND last_name = '{1}';"
			).format(name[0], name[1])
	return query_single (query)

def room_name_from_id (room_id):
	query = (
			"SELECT name "
			"FROM room "
			"WHERE room_id = {0};"
			).format(room_id)
	return query_single(query)

def room_id_from_name (room_name):
	query = (
			"SELECT room_id "
			"FROM room "
			"WHERE name = '{0}';"
			).format(room_name)
	return query_single(query)
	
def detail_name_from_id (detail_id):
	query = (
			"SELECT name "
			"FROM detail "
			"WHERE detail_id = {0};"
			).format(detail_id)
	DEBUG (query)
	return query_single(query)

	
	
	
## NPC INIT -------------------------------------------------------------------
def map_npcs (npc_ids, room_ids, murderer_ids):
	count = len (npc_ids)
	rooms_count = len(room_ids)
	
	for i in range(count):
		mapped_id  = i + 1
		npc_id = npc_ids[i]
		room_id = room_ids[i % rooms_count]
		if npc_id in murderer_ids:
			state = 'murdering'
		else:
			state = 'not murderer'
		
		insert = "INSERT INTO mapped_npc VALUES ({0}, {1}, {2}, '{3}');".format(mapped_id, npc_id, room_id, state)

		run_update(insert)


def get_murderers (sub_A, sub_B):
	query = (
			"SELECT npc_id FROM npc "
			"WHERE (map_group = 'A' AND sub_group = {0}) "
				"OR (map_group = 'B' AND sub_group = {1});"
			).format(sub_A, sub_B)
	return column_as_list (run_query(query), 0)

	

	
	
## NPC CONTROLLING ------------------------------------------------------------
def get_living_npcs ():
	query = ("SELECT mapped_id FROM mapped_npc "
			"WHERE mapped_id NOT IN (SELECT victim FROM murder);")
	return column_as_list(run_query(query), 0)

def get_npc_location (mapped_id):
	query = (
			"SELECT location "
			"FROM mapped_npc "
			"WHERE mapped_id = {0};"
			).format(mapped_id)
	return query_single(query)

def move_npc (mapped_id, room_id):
	update = "UPDATE mapped_npc SET location = {0} WHERE mapped_id = {1};".format(room_id, mapped_id)
	run_update (update)

	
	
	
	
	
## MURDERING ------------------------------------------------------------------
def get_active_murderers ():
	query = (
			"SELECT mapped_id FROM mapped_npc "
			"WHERE state = 'murdering' "
			"AND mapped_id NOT IN "
				"(SELECT victim FROM murder) "
			"ORDER BY mapped_id;"
			)
	return column_as_list (run_query(query), 0)
	
# Next two methods would profit from yield structure
def rooms_in_order (first_room):
	room_count = query_single ("SELECT COUNT(*) FROM room;")
	rooms = [first_room]
	
	# Add rooms to list in order
	# Take room at current index and get all rooms adjacent to it
	# If they are not in list already, add them
	for i in range(room_count):
		other_rooms = get_adjacent_rooms(rooms[i])
		for item in other_rooms:
			if not item in rooms:
				rooms.append(item)
				
	return rooms
	
def get_targets(murderer_mapped_id):
	rooms = rooms_in_order(get_npc_location(murderer_mapped_id))
	targets = None
	
	# Loop through rooms in order and return all npcs in first room that is not empty
	for i in range (len(rooms)):
		targets = live_npcsid_in_room(rooms[i])
		
		if murderer_mapped_id in targets:
			targets.remove(murderer_mapped_id)
			
		if targets != None and targets != []:
			room = rooms[i]
			break
	
	if targets == []:
		targets = None
		
	return targets
	
def murder(victim_mapped_id, murderer_mapped_id):
	insert = "INSERT INTO murder VALUES ({0}, {1});".format(victim_mapped_id, murderer_mapped_id)
	run_update (insert)
	
def add_clue (victim_mapped_id, witness_mapped_id, detail_id):
	insert = "INSERT INTO clue VALUES ({0}, {1}, {2});".format(victim_mapped_id, witness_mapped_id, detail_id)
	run_update (insert)
	
	
	
## MOVE FUNCTIONS -------------------------------------------------------------
def get_room_id (target):
	query = (
			"SELECT room_id "
			"FROM room "
			"WHERE name = '{0}';"
			).format(target)
	return query_single(query)
	
def get_adjacent_rooms (room_id):
	query = (
			"SELECT to_id "
			"FROM passage "
			"WHERE from_id = '{0}';"
			).format(room_id)
	return column_as_list(run_query(query), 0)


def get_available_directions(room_id):
	query = (
			"SELECT direction "
			"FROM passage "
			"WHERE from_id = '{0}';"
			).format(room_id)
	return column_as_list(run_query(query), 0)

def get_target_room_id (target):
	query = (
			"SELECT to_id "
			"FROM passage "
			"WHERE direction = '{0}';"
			).format(target)
	return query_single(query)
	
def get_room_in_direction(start_room_id, direction):
	query = (
			"SELECT to_id FROM passage "
			"WHERE from_id = {0} AND direction = '{1}';"
			). format(start_room_id, direction)
	return query_single(query)
	
def get_room_name (room_id):
	query = (
			"SELECT name "
			"FROM room "
			"WHERE room_id = '{0}';"
			).format(room_id)
	return query_single(query)

def get_direction (from_id, to_id):
	return query_single(
						"SELECT direction FROM passage "
						"WHERE from_id = {0} "
						"AND to_id = {1};".format(from_id, to_id)
						)

def find_path (from_id, to_id):
	if from_id == to_id:
		return None
	else:
		route = None
		routes = [[from_id]]
		used = [from_id]
		
		while route is None:
			count = len (routes)
			for i in range (count):
				for room_id in get_adjacent_rooms(routes [i][-1]):
					if not room_id in used:
						if room_id == to_id:
							route = routes [i]
							route.append(room_id)
							break
						else:
							routes.append(routes[i][:])
							routes[-1].append(room_id)
							used.append(room_id)
						
				if route:
					break
			
			routes = routes [count:]
			
		route_directions = [(route[i+1], get_direction(route[i], route[i+1])) for i in range(len(route)- 1)]

		return route_directions
		

	
## LOOK FUNCTIONS -------------------------------------------------------------
def live_npcsid_in_room (room_id):
	query = (
			"SELECT mapped_id FROM mapped_npc "
			"WHERE mapped_id NOT IN (SELECT victim FROM murder)"
			"AND location = {0};"
			).format (room_id)			

	return column_as_list(run_query(query), 0)	
	
def dead_npcsid_in_room (room_id):
	query = (
			"SELECT mapped_id FROM mapped_npc "
			"WHERE mapped_id IN (SELECT victim FROM murder)"
			"AND location = {0};"
			).format (room_id)
	return column_as_list(run_query(query), 0)

def live_npcs_in_room (room_id):
	query = (
			"SELECT first_name, last_name "
			"FROM npc "
			"WHERE npc_id NOT IN("
				"SELECT npc.npc_id "
				"FROM murder "
				"INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim "
				"INNER JOIN npc ON npc.npc_id = mapped_npc.npc "
				"WHERE mapped_npc.location = '" + str(room_id) + "');")
	return run_query(query)

def dead_npcs_in_room (room_id):
	query = (
			"SELECT first_name, last_name "
			"FROM npc "
			"WHERE npc_id IN("
				"SELECT npc.npc_id "
				"FROM murder "
				"INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim "
				"INNER JOIN npc ON npc.npc_id = mapped_npc.npc "
				"WHERE mapped_npc.location = '" + str(room_id) + "');")
	return run_query(query)

def id_from_name (target):
	query = "SELECT npc_id FROM mapped_npc INNER JOIN npc ON mapped_npc.npc = npc.npc_id WHERE first_name = '{0}' AND last_name = '{1}';".format(target[0], target[1])
	return query_single(query)

def get_details (mapped_id):
	query = (
			"SELECT detail FROM npc_detail "
			"INNER JOIN mapped_npc ON mapped_npc.npc = npc_detail.npc "
			"WHERE mapped_id = {0};"
			).format(mapped_id)
	return column_as_list (run_query(query), 0)

def get_adjacent_rooms_and_directions(room_id):
	query = (
			"SELECT to_id, direction "
			"FROM passage "
			"WHERE from_id = {0}"
			).format(room_id)
	return run_query(query)
	


	
## ASK FUNCTIONS --------------------------------------------------------------
def dead_npcs ():
	query = (
			"SELECT first_name, last_name "
			"FROM npc "
			"WHERE npc_id IN("
				"SELECT npc.npc_id "
				"FROM murder "
				"INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim "
				"INNER JOIN npc ON npc.npc_id = mapped_npc.npc);")
	return run_query(query)

def live_npcs ():
	query = (
			"SELECT first_name, last_name "
			"FROM npc "
			"WHERE npc_id NOT IN("
				"SELECT npc.npc_id "
				"FROM murder "
				"INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim "
				"INNER JOIN npc ON npc.npc_id = mapped_npc.npc);")
	return run_query(query)
	
def solved_murder():
	query = (
			"SELECT mapped_id "
			"FROM murder "
			"INNER JOIN mapped_npc "
			"WHERE state = 'arrested';")
	return query_single(query)

def murderer_detail (witness, victim):
	#DEBUG((witness, victim))
	query = (
			"SELECT detail.name "
			"FROM detail "
			"INNER JOIN clue ON clue.detail = detail.detail_id "
			"WHERE witness = {0} AND victim = {1};"
			).format(npc_id_from_name(witness), npc_id_from_name(victim))
			
	# JOEL TEIN KOKEILUU		
	query = "SELECT detail FROM clue WHERE witness = {0} AND victim = {1};".format(npc_id_from_name(witness), npc_id_from_name(victim))
	result = run_query(query)
	if result == []:
		return None
	else:
		return column_as_list(result, 0) #Multiple details? What then?
	
def current_victims_murderer_id (victim):
	query = (
			"SELECT mapped_id "
			"FROM mapped_npc "
			"INNER JOIN murder ON mapped_id = murder.murderer "
			"WHERE murder.victim = {0};"
			).format(npc_id_from_name(victim))
	return query_single(query)
	

def other_witnessed_victims(witness_mapped_id, murderer_mapped_id):
	query = (
			"SELECT DISTINCT murder.victim"
			" FROM murder"
			" INNER JOIN clue ON clue.victim = murder.victim"
			" WHERE murderer = {0} AND witness = {1};"
			).format (murderer_mapped_id, witness_mapped_id)
	return column_as_list(run_query(query), 0)

def witnessed_multiple_murders (victim): #by the current victim's murderer
	
	query = (
			"SELECT clue.witness "
			"FROM clue "
			"WHERE clue.victim IN ("
				"SELECT mapped_id "
				"FROM mapped_npc "
				"INNER JOIN murder ON mapped_id = murder.victim "
				"WHERE murder.murderer IN ({0})) "
			"GROUP BY victim;"
			).format(current_victims_murderer_id(victim))
	return column_as_list(run_query(query), 0)
	
def all_but_current_murder_victims(victim):
	query = (
			"SELECT mapped_id "
			"FROM mapped_npc "
			"INNER JOIN murder ON mapped_id = murder.victim "
			"WHERE murder.murderer IN ({0}) AND mapped_id != {1}"
			).format(current_victims_murderer_id(victim), npc_id_from_name(victim))
	return column_as_list(run_query(query), 0)

## PLAYER NOTES ---------------------------------------------------------------
def get_notes():
	result = run_query (
					"SELECT DISTINCT player_clue.victim, detail, state "
					"FROM player_clue "
					"INNER JOIN murder ON murder.victim = player_clue.victim "
					"INNER JOIN mapped_npc ON mapped_id = murder.murderer;"
					)
	notes = []
	for record in result:
		next_victim = record[0]
		if notes == [] or notes [-1][0] != next_victim:
			location = get_npc_location(next_victim)
			solved = record[2] == 'arrested'
			notes.append((next_victim, location, [], solved))
			
		if record [1]:
			notes[-1][2].append(record[1])
	return notes

def infinite_index():
	index = 0
	while True:
		index += 1
		yield index
	
def add_player_clue(victim, detail):
	if not detail:
		detail = 'null'
	query = "INSERT INTO player_clue VALUES ({0}, {1});".format(victim, detail)
	run_update(query)



