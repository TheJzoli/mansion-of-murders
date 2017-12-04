# NPC Tool
# © Leo Tamminen, leo.tamminen@metropolia.fi

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

print (
		"Welcome to NPC Tool.\n\n"
		
		" 'n'	add name\n"
		" 'd'	edit description\n"
		" 's'	show all\n"
		" 'r'	remove person\n"
		" 'l'	load NPCs from database\n"
		" 'e'	exit\n"
		)
		
		
cmd_add_person = ['n']
cmd_add_description = ['d']
cmd_show = ['s']
cmd_remove = ['r']
cmd_load = ['l']
cmd_exit = ['e']

commands = ['n','d','s','r','l','e']

cmd_yes = ['y', 'Y']
char_removables = [' ']

names = []
longest_length = 0
descriptions = []
max_chars_in_description = 30

generic_description = "Generic description."

command = None
while not command in cmd_exit:
	
	command = None
	while command is None:
		command = input(">>> ").lower()
	
	if command in cmd_add_person:
		names_input = input("Enter full names separated with comma:\n\n").lower().split(sep = ',')
		
		added_names = []
		for name in names_input:
			name = name.split()
			if len(name) == 2:
				names.append(name)
				descriptions.append(generic_description)
				added_names.append (name)
		
		print ("Added: {0}".format(added_names))
	
	elif command in cmd_add_description:
		
		target = input("\nWhose description do you want to edit? Enter full name:\n\n").lower().split()
		if len(target) == 2 and target in names:
			index = names.index(target)
			print ("\nCurrent description: {0}".format(descriptions[index]))
			confirm = trim(input("Edit? (y)"))
			
			if confirm in cmd_yes:
				description = trim(input("\nEnter new description:\n\n"))
			
				if len(description) > 0:
					descriptions[index] = description
					print ("Done!")
		
	elif command in cmd_show:
	
		count = len(names)
		printout = ""
		for i in range(count):
			index = i + 1
			first_name = names[i][0][0].upper() + names[i][0][1:]
			last_name = names[i][1][0].upper() + names[i][1][1:]
			name = "{0} {1}".format(first_name, last_name)
			
			if len(descriptions[i]) > max_chars_in_description:
				description = descriptions[i][:max_chars_in_description - 3] + "..."
			else:
				description = descriptions[i]
			
			printout += "{0:3} {1:{2}} {3}\n".format(index, name, longest_length + 1, description)
		
		print(printout)
		
	elif command in cmd_remove:
		print ("Remove")
		
		
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