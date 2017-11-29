# Room Tool
# © Leo Tamminen, leo.tamminen@metropolia.fi

from operator import itemgetter

def trim (text):
	while len(text) > 0 and text [0] in char_removables:
		text = text[1:]
	while len(text) > 0 and text[-1] in char_removables:
		text = text[:-1]
	return text


def input_list (message):
	words = input(message).lower().split(sep=',')
	
	processed_words = []
	for word in words:
		processed_words.append (trim(word))
		
	return processed_words

def sort_connections (give_connections):
	sorted_connections = []
	for entry in give_connections:
		sort_items = []
		for item in entry:
			sort_items.append ([rooms.index (item[0]), item[0], item[1]])
		
		sort_items.sort(key = itemgetter (1))
		
		sorted_connections.append ([])
		for item in sort_items:
			sorted_connections[-1].append ([item [1], item [2]])
		
	return sorted_connections
		
print (
		"Welcome to Room Tool.\n\n"
		
		" 'r'/'rooms'	add rooms\n"
		" 'c'/'connect'	connect rooms\n"
		" 's'/'show'	show all\n"
		" 'd'/'delete'	delete room\n"
		" 'l'/'load'	load rooms from database\n"
		" 'e'/'exit'	exit\n"
		)
		
cmd_add_rooms = ['r', 'room']
cmd_add_connection = ['c', 'connect']
cmd_show = ['s', 'show']
cmd_print = ['p', 'print']
cmd_delete = ['d', 'delete']
cmd_exit = ['e', 'exit']
cmd_database = ['l', 'load']
commands = cmd_add_rooms + cmd_add_connection + cmd_show + cmd_print + cmd_delete + cmd_exit + cmd_database

char_removables = [' ']
cmd_yes = ['y', 'Y']

longest_length = 0
rooms = []
connections = []

possible_directions = ['u','d','n','e','s','w','ne','se','nw','sw']
opposite_directions = ['d','u','s','w','n','e','sw','nw','se','ne']

## PROGRAM LOOP
command = None
while not command in cmd_exit:

	command = None
	while not command in commands:
		command = input ("\n>> ").lower()
		
	## ADD ROOMS --------------------------------------------------------------
	if command in cmd_add_rooms:
		
		words = input_list ("Enter room names, separated by comma: \n\n")
		added = []
		not_added = []
		for room in words:
			parts = len(room.split())
			if room != "":
				if parts <= 2:
					rooms.append (room)
					connections.append([])
					if len(room) > longest_length:
						longest_length = len(room)
					added.append(room)
				else:
					not_added.append(room)
	
		print ("Added: {0}".format(added))
		if len(not_added) > 0:
			print ("Too many parts, could not add: {0}".format(not_added))
	
	## CONNECT ROOMS ----------------------------------------------------------
	elif command in cmd_add_connection:
		room_name = trim(input("Add connections to which room? "))
		if room_name in rooms:
			
			index = rooms.index(room_name)
			print ("{0}: {1}".format(rooms[index], connections[index]))
		
			command = 'y'
			while command in cmd_yes:
				
				room_to_add = None
				while not (room_to_add in rooms or room_to_add == ""):
					room_to_add = trim(input("Enter room name: "))
				
				direction_to_add = None
				if room_to_add != "":
					while not (direction_to_add in possible_directions or direction_to_add == ""):
						direction_to_add = trim(input("Enter direction: "))
				
				
				if room_to_add != "" and direction_to_add != "":
					
					exists = False
					for item in connections [index]:
						if item[0] == room_to_add:
							exists = True
					
					if not exists:
						# Add this side if connection
						connections [index].append ([room_to_add, direction_to_add])
						
						# Also add other side
						opposite_direction = opposite_directions [possible_directions.index(direction_to_add)]
						opposite_index = rooms.index(room_to_add)
						connections [opposite_index].append([room_name, opposite_direction])
						
						print ("Added connection between {0} and {1}.".format (room_name, room_to_add))
					
					else:
						print ("That connection already exists. To change direction, delete room first, then add and connect again")
					
					command = trim(input("\nAdd other connection to {0}? (y) ".format(room_name)))					
				else:
					command = None
		else:
			print ("There is no such room.")
	
	## PRINT SQL --------------------------------------------------------------
	elif command in cmd_print:
		confirm = input ("Print SQL-queries? (y) ")
		
		if confirm == 'Y' or confirm == 'y':
			connections = sort_connections(connections)
			
			printout_rooms = ""
			printout_passages = ""
			
			length = len(rooms)
			for i in range (length):
				from_index = i + 1
				printout_rooms += "INSERT INTO room VALUES ({0}, '{1}', NULL);\n".format(from_index, rooms [i])
				
				room_words = rooms[i].split()
				if len(room_words) == 2:
					printout_rooms += "INSERT INTO two_part_words VALUES ('{0}', '{1}');\n".format(room_words[0], room_words[1])
				
				printout_passages += "-- {0}\n".format(rooms[i])
				count = len(connections [i])
				for j in range (count):
					to_index = rooms.index(connections[i][j][0]) + 1
					direction = connections[i][j][1]
					
					printout_passages += "INSERT INTO passage VALUES ({0}, {1}, '{2}');\n".format(from_index, to_index, direction);
			
			print()
			print(printout_rooms)
			print()
			print(printout_passages)
			
	## PRINT IN CONSOLE -------------------------------------------------------
	elif command in cmd_show:
		connections = sort_connections(connections)
		for i in range (len(rooms)):
			print ("{0:{1}}: {2}".format(rooms[i], longest_length, connections[i]))
	
	## DELETE -----------------------------------------------------------------
	elif command in cmd_delete:
		room_name = trim(input("Delete which room? "))
		if room_name in rooms:
			confirm = input ("Delete '{0}' and connections? (y) ".format(room_name))
			if confirm == 'Y' or confirm == 'y':
				index = rooms.index(room_name)
				del rooms[index]
				
				
				length = len(connections[index])
				for i in range(length):
					
					other_index = rooms.index(connections[index][i][0])
					other_length = len(connections[other_index])
					print (connections[other_index])
					print ("len " + str(other_length))
					for j in range (other_length):
						print (j)
						other_item = connections[other_index][j]
						if other_item [0] == room_name:
							print (connections[other_index])
							print (other_item)
							connections[other_index].remove(other_item)
				
				del connections [index] 
		else:
			print ("There is no such room.")
	
	## LOAD FROM DATABASE -----------------------------------------------------
	elif command in cmd_database:
		confirm = trim(input("Load Rooms and Passages from database? (y) "))
		
		if rooms != [] and confirm in cmd_yes:
			confirm = trim(input("This will cause current rooms and connections to lose. Continue? (y) "))
			
		if confirm in cmd_yes:
			rooms = []
			connections = []
			longest_length = 0
			
			print ("....")
			
			import mysql.connector
			database = mysql.connector.connect(
								host = 'localhost',
								user = 'dbuser',
								passwd = 'dbpass',
								db = 'mom_game',
								buffered = True)
			cursor = database.cursor()
			
			rooms_query = "SELECT name FROM room ORDER BY room.room_id;"
			cursor.execute(rooms_query)
			rooms_result = cursor.fetchall()

			passage_query = (
								"SELECT f.name, t.name, direction "
								"FROM passage "
								"INNER JOIN room AS f ON f.room_id = passage.from_id "
								"INNER JOIN room AS t ON t.room_id = passage.to_id "
								"ORDER BY f.room_id;"
							)
			cursor.execute(passage_query)
			passage_result = cursor.fetchall()
			
			
			for record in rooms_result:
				rooms.append (record[0])
				connections.append ([])
				if len(record[0]) > longest_length:
					longest_length = len(record [0])
	

			for record in passage_result:
				index = rooms.index (record[0])
				connections[index].append([record[1], record[2]])
		
		database.rollback()
		database.close()
		
		print ("Loaded!\n")
	
	## CONFIRM EXIT -----------------------------------------------------------
	elif command in cmd_exit:
		confirm = trim(input("All data will be lost. Do you want to quit? (y) "))
		if not confirm in cmd_yes:
			command = None
		else:
			print ("Good Riddance!\n")
		
## END PROGRAM LOOP
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	