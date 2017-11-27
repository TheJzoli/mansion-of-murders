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
	
## SQL FUNCTIONS
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
	

## PARSER FUNCTIONS
def get_two_part_word (word):
	query = "SELECT word_2 FROM two_part_words WHERE word_1 = '{0}'".format(word)
	result = run_query (query)
	if result:
		return column_as_list (result, 0)
	else:
		return None

def get_verbs():
	query = "SELECT word FROM verb_synonyms;"
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

# [0] is first name, [1] is last name
def get_npcs ():
	query = "SELECT first_name, last_name FROM npc;"
	result = run_query (query);
	return [column_as_list(result, 0), column_as_list (result, 1)]
	
# [0] are short cuts and [1] are full names
def get_directions ():
	query = "SELECT direction_id, name FROM direction;"
	result = run_query (query)
	return [column_as_list(result, 0), column_as_list (result, 1)]

	
## CONVERSIONS
def long_direction (short_direction):
	query = "SELECT name FROM direction WHERE direction_id = '{0}';".format(short_direction)
	return run_query(query)[0][0]

def short_direction(long_direction):
	query = "SELECT direction_id FROM direction WHERE name = '{0}';".format(long_direction)
	return run_query(query)[0][0]
	
## MOVE FUNCTIONS
def get_room_id (target):
	query = "SELECT room_id FROM room WHERE name = '" + target + "';"
	return query_single(query)


## LOOK FUNCTIONS

## ASK FUNCTIONS
	
	
	
	
	