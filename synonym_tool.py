print ("Welcome to Synonmys adding tool!\n")

print (
				"'W'\tchange word\n"
				"'A'\tadd synonyms\n"
				"'S'\tshow\n"
				"'P'\tprint SQL-queries\n"
				"'C'\tclear\n"
				"'E'\texit\n"
				)

cmd_word = ['W', 'w']
cmd_synonym = ['A', 'a']
cmd_show = ['S', 's']
cmd_print = ['P', 'p']
cmd_clear = ['C', 'c']
cmd_exit = ['E', 'e', 'exit']
commands = cmd_word + cmd_synonym + cmd_show + cmd_print + cmd_clear + cmd_exit

answer_yes = ['Y', 'y']
char_removables = [' ']

main_word = None
synonyms = []
longest_length = 0


## MAIN LOOP
command = None
while not command in cmd_exit:

	command = None
	while command not in commands:
		command = input("> ")
	
	# Just add space
	print()
	
	if command in cmd_word:
		change = True
		if main_word != None:
			confirm = input("Current word is '{0}'. Do you want to change it? (y) ".format(main_word))
			change = confirm in answer_yes
		
		if change:
			word = input ("Enter word for synonyms: ").lower()
			if len (word) > 0:
				main_word = word
			
	elif command in cmd_synonym:
		if main_word != None:
			words = input ("Enter synonyms for '{0}', separated by commas\n\n> ".format(main_word))
			words = words.lower().split(sep = ',')
			
			processed_words = []
			for word in words:
				
				if len(word) > 0:
					while word[0] in char_removables:
						word = word[1:]
					while word[-1] in char_removables:
						word = word[:-1]
												
					processed_words.append(word)
					
					if len(word) > longest_length:
						longest_length = len(word)
					
			synonyms += processed_words
			print (" Added: {0}".format(processed_words))
			
	elif command in cmd_show:
		print ("Current word is '{0}'.".format(main_word))
		print ("Synonmys are: {0}".format(synonyms))
		
	elif command in cmd_print:
		confirm = input ("Print SQL-queries? (y) ")
		
		if confirm == 'Y' or confirm == 'y':
			
			# Just add space
			print()
			
			for item in synonyms:
				formatted_item = "'{0}',".format(item)
				query = "INSERT INTO synonyms VALUES ({0:{1}} '{2}');".format(formatted_item, longest_length + 3, main_word)
				print (query)
				
				words = item.split()
				if len(words) > 1:
					query = "INSERT INTO two_parts_words VALUES ('{0}', '{1}');".format(words[0], words[1])
					print (query)
	
	elif command in cmd_clear:
		confirm = input ("Clear word and synonyms? All will be lost (y) ")
		
		if confirm == 'Y' or confirm == 'y':
			main_word = None
			synonyms = []
			longest_length = 0
			print ("Cleared!")
		else:
			print ("Not cleared")
		
	# Just add space
	print()
## END MAIN LOOP

input ("Press ENTER to exit")			
print("Good Riddance!")			
			
			
			
			
			
			

			
			