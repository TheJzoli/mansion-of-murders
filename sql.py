import mysql.connector

def DEBUG(message):
	print("SQL DEBUG: " + str(message));

default = "SELECT message FROM error;"

## DATABASE
database = mysql.connector.connect(
	host = 'localhost',
	user = 'dbuser',
	passwd = 'dbpass',
	db = 'mom_game',
	buffered = True)
DEBUG ("Connect to sql")

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
	
# [0] is first name, [1] is last name
def get_npcs_names ():
	query = "SELECT first_name, last_name FROM npc;"
	result = run_query (query)
	return [column_as_list(result, 0), column_as_list (result, 1)]
	
# [0] are short cuts and [1] are full names
def get_directions ():
	query = "SELECT direction_id, name FROM direction;"
	result = run_query (query)
	return [column_as_list(result, 0), column_as_list (result, 1)]

def get_full_name (name):
	# This is not complete, and works only when no same first or last name exist
	all_names = get_npcs ()
	first_name = False
	last_name = False

	for i in range(len(all_names)):
		
		# case john wilsom and john johnson
		if name == all_names[i][0]:
			first_name = name
			if last_name == False:
				last_name = all_names [i][1]
			else:
				last_name = None
			
			
		# case john wilson and maria wilson
		elif name == all_names [i][1]:
			last_name = name
			if first_name == False:
				first_name = all_names[i][0]
			else:
				first_name = None
	
	return first_name, last_name
	
	
	
	
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

def room_id_from_name (room_name):
	query = (
			"SELECT room_id "
			"FROM room "
			"WHERE name = '{0}';"
			).format(room_name)
	return query_single(query)

	
## MOVE FUNCTIONS -------------------------------------------------------------
def get_room_id (target):
	query = "SELECT room_id FROM room WHERE name = '{0}';".format(target)
	return query_single(query)
	
def get_adjacent_rooms (room_id):
	query = "SELECT to_id FROM passage WHERE from_id = '{0}';".format(room_id)
	return column_as_list(run_query(query), 0)

def get_available_directions(room_id):
	query = "SELECT direction FROM passage WHERE from_id = '{0}';".format(room_id)
	return column_as_list(run_query(query), 0)

def get_target_room_id (target):
	query = "SELECT to_id FROM passage WHERE direction = '{0}';".format(target)
	return query_single(query)
	
def get_room_name (room_id):
	query = "SELECT name FROM room WHERE room_id = '{0}';".format(room_id)
	return query_single(query)

	
	
## LOOK FUNCTIONS -------------------------------------------------------------
'''
def live_npcsid_in_room (room_id):
	query = "SELECT npc.npc_id FROM npc WHERE npc.npc_id NOT IN(SELECT npc.npc_id FROM murder INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim INNER JOIN npc ON npc.npc_id = mapped_npc.npc WHERE mapped_npc.location = '" + str(room_id) + "');"
	return column_as_list(run_query(query), 0)
'''
	
def live_npcsid_in_room (room_id):
	query = (
			"SELECT mapped_id FROM mapped_npc "
			"WHERE mapped_id NOT IN (SELECT victim FROM murder)"
			"AND location = {0};"
			).format (room_id)			

	return column_as_list(run_query(query), 0)	
	
def dead_npcsid_in_room (room_id):
	query = "SELECT npc.npc_id FROM murder INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim INNER JOIN npc ON npc.npc_id = mapped_npc.npc WHERE mapped_npc.location ='" + str(room_id) + "';"
	return column_as_list(run_query(query), 0)

def live_npcs_in_room (room_id):
	query = "SELECT first_name, last_name FROM npc WHERE npc_id NOT IN(SELECT npc.npc_id FROM murder INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim INNER JOIN npc ON npc.npc_id = mapped_npc.npc WHERE mapped_npc.location = '" + str(room_id) + "');"
	return run_query(query)

def dead_npcs_in_room (room_id):
	query = "SELECT first_name, last_name FROM npc WHERE npc_id IN(SELECT npc.npc_id FROM murder INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim INNER JOIN npc ON npc.npc_id = mapped_npc.npc WHERE mapped_npc.location = '" + str(room_id) + "');"
	return run_query(query)

def id_from_name (target):
	query = "SELECT npc_id FROM mapped_npc INNER JOIN npc ON mapped_npc.npc = npc.npc_id WHERE first_name = '{0}' AND last_name = '{1}';".format(target[0], target[1])
	return query_single(query)
	
	
	
## ASK FUNCTIONS --------------------------------------------------------------
def dead_npcs ():
	query = "SELECT first_name, last_name FROM npc WHERE npc_id IN(SELECT npc.npc_id FROM murder INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim INNER JOIN npc ON npc.npc_id = mapped_npc.npc);"
	return run_query(query)

def live_npcs ():
	query = "SELECT first_name, last_name FROM npc WHERE npc_id NOT IN(SELECT npc.npc_id FROM murder INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim INNER JOIN npc ON npc.npc_id = mapped_npc.npc);"
	return run_query(query)

def murderer_detail (witness, victim):
	#DEBUG((witness, victim))
	query = (
			"SELECT detail.name "
			"FROM detail "
			"INNER JOIN clue ON clue.detail = detail.detail_id "
			"WHERE witness = {0} AND victim = {1};"
			).format(npc_id_from_name(witness), npc_id_from_name(victim))
	result = run_query(query)
	if result == []:
		return None
	else:
		return column_as_list(result, 0) #Multiple details? What then?
	
def current_victims_murderer_id (victim):
	query = "SELECT mapped_id FROM mapped_npc INNER JOIN murder ON mapped_id = murder.murderer WHERE murder.victim = {0};".format(npc_id_from_name(victim))
	return query_single(query)
	
def witnessed_multiple_murders (victim): #by the current victim's murderer
	query = "SELECT clue.witness FROM clue WHERE clue.victim IN (SELECT mapped_id FROM mapped_npc INNER JOIN murder ON mapped_id = murder.victim WHERE murder.murderer IN ({0})) GROUP BY victim;".format(current_victims_murderer_id(victim))
	return column_as_list(run_query(query), 0)