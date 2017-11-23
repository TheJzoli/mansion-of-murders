import mysql.connector

## DATABASE
database = mysql.connector.connect(
	host = 'localhost',
	user = 'dbuser',
	passwd = 'dbpass',
	db = 'mom_game',
	buffered = True)

## SQL FUNCTIONS
def run_query (query):
	cursor = database.cursor()
	cursor.execute (query)
	return cursor.fetchall()

def get_adjacent_rooms (room_id):
	#query = "SELECT name FROM room INNER JOIN passage WHERE from_id = {0};".format (room_id)
	query = "SELECT to_id FROM passage WHERE from_id = {0};".format(room_id)
	return run_query(query)[0]
	
def get_room_id (room_name):
	query = "SELECT room_id FROM room WHERE name = '{0}';".format(room_name)
	return run_query(query)[0][0]

def get_room_name (room_id):
	query = "SELECT name FROM room WHERE room_id = {0};".format(room_id)
	return run_query(query)[0][0]