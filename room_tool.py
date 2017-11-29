#Room Tool
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

def sort_connections ():
	for room_index in range(len(connections)):
		entry = connections[room_index]
		length = len(entry)
		for i in range (length - 1):
		
			smallest_index = 1000
		
			for j in range (i, length):
				index = rooms.index(entry[j][0])
				if index < smallest_index:
					smallest_index = index
			
			if smallest_index != i:
				entry[i], entry[smallest_index] = entry [smallest_index], entry [i]
				
		connections [room_index] = entry
		
print (
		"Welcome to Room Tool.\n\n"
		" 'r'/'rooms'	add rooms\n"
		" 'c'/'connect'	connect rooms\n"
		" 's'/'show'	show all\n"
		" 'd'/'delete'	delete room\n"
		" 'e'/'exit'	exit\n"
		)
		
cmd_add_rooms = ['r', 'room']
cmd_add_connection = ['c', 'connect']
cmd_show = ['s', 'show']
cmd_print = ['p', 'print']
cmd_delete = ['d', 'delete']
cmd_exit = ['e', 'exit']
commands = cmd_add_rooms + cmd_add_connection + cmd_show + cmd_print + cmd_delete + cmd_exit

char_removables = [' ']
cmd_yes = ['y', 'Y']

longest_length = 0
rooms = []
connections = []

## FOR DEBUG
longest_length = len('kitchen')
rooms = ['kitchen','hall', 'pool']
connections = [[['pool','nw'],['hall', 'e']],[['kitchen', 'w']],[['kitchen', 'se']]]

print (connections)

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
		for room in words:
			if (room != ""):
				rooms.append (room)
				connections.append([])
				if len(room) > longest_length:
					longest_length = len(room)
	
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
			sort_connections()
			
			printout_rooms = ""
			printout_passages = ""
			
			length = len(rooms)
			for i in range (length):
				from_index = i + 1
				printout_rooms += "INSERT INTO room VALUES ({0}, '{1}', NULL);\n".format(from_index, rooms [i])
				
				printout_passages += "-- {0}\n".format(rooms[i])
				count = len(connections [i])
				for j in range (count):
					to_index = rooms.index(connections[i][j][0]) + 1
					direction = connections[i][j][1]
					
					printout_passages += "INSERT INTO passage VALUES ({0}, {1}, '{2}');\n".format(from_index, to_index, direction);
			
			print(printout_rooms)
			print()
			print(printout_passages)
			
	## PRINT IN CONSOLE -------------------------------------------------------
	elif command in cmd_show:
		sort_connections()
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
					for i in range (other_length):
						other_item = connections[other_index][i]
						if other_item [0] == room_name:
							print (connections[other_index])
							print (other_item)
							connections[other_index].remove(other_item)
				
				del connections [index] 
		else:
			print ("There is no such room.")
	

## END PROGRAM LOOP
	
	