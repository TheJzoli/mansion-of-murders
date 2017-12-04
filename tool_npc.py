# NPC Tool
# © Leo Tamminen, leo.tamminen@metropolia.fi

import math

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
	
def format_name(name):
	first_name = name[0][0].upper() + name[0][1:]
	last_name = name[1][0].upper() + name[1][1:]
	return "{0} {1}".format(first_name, last_name)
	
def divide_to_parts(count, parts):
	count = math.ceil(count)
	for i in range (count):
		yield int(i/(count/parts)) + 1

def indices (list):
	count = len(list)
	for i in range (count):
		yield i + 1

def npc_index_input (text):
	target = input(text).lower().split()
	
	index = None
	
	if len(target) == 2 and target in names:
		index = names.index(target)

	elif len(target) == 1:
		try:
			target = int (target[0])
			if target in indices(names):
				index = target - 1
		except:
			pass
		
	return index
		
print (
		"Welcome to NPC Tool.\n\n"
		
		" 'n'	add name\n"
		" 'd'	edit description\n"
		" 's'	show all\n"
		" 'r'	remove person\n"
		" 'p'	print SQL-queries\n"
		" 'l'	load NPCs from database\n"
		" 'e'	exit\n"
		)

cmd_add_person = ['n', 'name']
cmd_add_description = ['d']
cmd_show = ['s']
cmd_remove = ['r']
cmd_print = ['p']
cmd_load = ['l', 'load']
cmd_exit = ['e', 'exit']

cmd_yes = ['y', 'Y']
char_removables = [' ']

names = []
longest_length = 0
descriptions = []
max_chars_in_description = 40

map_groups = ['A', 'B']
sub_groups = [1,2,3,4,5]

generic_description = "Generic description."

command = None
while not command in cmd_exit:
	
	command = None
	while command is None:
		command = input(">>> ").lower()
	
	## ADD NEW PERSON ---------------------------------------------------------
	if command in cmd_add_person:
		#names_input = input("Enter full names separated with comma:\n\n").lower().split(sep = ',')

		names_input = input_list("Enter full names separated with comma:\n\n")
		
		added_names = []
		for name in names_input:
			name = name.split()
			if len(name) == 2:
				names.append(name)
				descriptions.append(generic_description)
				added_names.append (name)
				length = len(name [0]) + len(name[1])
				if length > longest_length:
					longest_length = length
		
		print ("Added: {0}".format(added_names))
	
	## EDIT DESCRIPTION -------------------------------------------------------
	elif command in cmd_add_description:
		
		index = npc_index_input("\nWhose description do you want to edit? Enter full name or index:\n\n")
		
		if not index is None:
			print ("\n{0}\nCurrent description: {1}".format(format_name(names[index]), descriptions[index]))
			confirm = trim(input("Edit? (y)"))
			
			if confirm in cmd_yes:
				description = trim(input("\nEnter new description:\n\n"))
		
				if len(description) > 0:
					descriptions[index] = description
					print ("Done!")
		
	## PRINT IN CONSOLE -------------------------------------------------------
	elif command in cmd_show:
	
		count = len(names)
		printout = ""
		for i in range(count):
			index = i + 1
			name = format_name(names [i])
			
			if len(descriptions[i]) > max_chars_in_description:
				description = descriptions[i][:max_chars_in_description - 3] + "..."
			else:
				description = descriptions[i]
			
			printout += "{0:3} {1:{2}} {3}\n".format(index, name, longest_length + 1, description)
			
			# Add extra line after every tenth
			if (i + 1) % 10 == 0:
				printout += "\n"
		
		print(printout)
	
	## PRINT SQL --------------------------------------------------------------
	elif command in cmd_print:
		confirm = trim(input("Print SQL-queries? (y) "))
		
		if confirm in cmd_yes:
			printout = ""
			count = len(names)
			
			# Two map_groups, two sets of sub_groups
			map_group_indices = divide_to_parts (count, 2)
			sub_group_indices = [divide_to_parts(count/2, 5), divide_to_parts(count/2, 5)]
						
			for i in range(count):
				index = i + 1
				first_name = names[i][0]
				last_name = names[i][1]
				description = descriptions[i]
				
				map_group_index = map_group_indices.__next__() - 1
				map_group = map_groups[map_group_index]
				sub_group = sub_group_indices[map_group_index].__next__()
				
				printout += "INSERT INTO npc VALUES ({0}, '{1}', '{2}', '{3}', '{4}', {5});\n".format(index, first_name, last_name, description, map_group, sub_group)
	
			print(printout)	
	
	## REMOVE NPC -------------------------------------------------------------
	elif command in cmd_remove:
		index = npc_index_input("Which NPC you want to delete? Enter full name or index:\n\n")
		
		if not index is None:
			confirm = trim(input("Do you want to delete '{0}'? (y) ".format(format_name(names[index]))))
			
			if confirm in cmd_yes:
				del names[index]
				del descriptions[index]
				print ("Removed!")
				
				longest_length = 0
				for name in names:
					length = len(name[0]) + len(name[1])
					if length > longest_length:
						longest_length = length
			
	## LOAD FROM DATABASE -----------------------------------------------------
	elif command in cmd_load:
		confirm = trim(input("Load NPCs from database? (y) "))
		
		if names != [] and confirm in cmd_yes:
			confirm = trim(input("This will cause current NPCs to lose. Continue? (y) "))
			
		if confirm in cmd_yes:
			names = []
			descriptions = []
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
			
			query = "SELECT first_name, last_name, description FROM npc ORDER BY npc_id ASC;"
			cursor.execute (query)
			result = cursor.fetchall()
			
			for record in result:
				names.append([record[0], record[1]])
				#print (names [-1], end = "\t")
				
				length = len(names[-1][0]) + len(names [-1][1])
				if length > longest_length:
					longest_length = length
				
				descriptions.append (record[2])
				#print (descriptions[-1])
			
		database.rollback()
		database.close()
		
		print ("Loaded!\n")