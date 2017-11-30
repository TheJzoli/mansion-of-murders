'''
# These are all populated from master.py
rooms = [] 				# Names of rooms
npcs = []				# Npcs full name in list = ["firstname", "secondname"]
first_names = []		# only first names in list
last_names = []			# only last names in list
player					# player instance, holds location
'''
import sql

#onko jo olemassa



def look(target):

	live_npcsid_in_room = sql.live_npcsid_in_room(player.location)
	dead_npcsid_in_room = sql.dead_npcsid_in_room(player.location)
	#room_id = sql.get_room_id(player.location)


	message = ""
	if(target in rooms):
			## Noora muutin ja siirsin tän tänne
			room_id = sql.get_room_id(target)
			if(room_id == player.location):
					
					## Noora tee sileen et tää osio, ja toi look around ois sama,
					## Tyyliin et tää vaan kutsuu look_around()
			
					query = "SELECT description FROM room WHERE room.room_id ='" + str(room_id) + "';"
					result = sql.query_single(query)
					message = result
					
					## Tää on testi vaa, kun ei oo nitä descriptioneja vielä
					if message == None:
						message = "{0} is rather nice.".format(target)
			else:
					message = "You can't look there from here."
	elif(target in npcs):
			
			## NOORA laitoin vaan tän tähän
			id_from_name = sql.id_from_name(target)
			
			if(id_from_name in live_npcsid_in_room):
					query = "SELECT description FROM npc WHERE npc_id = " + str(id_from_name) + ";"
					result = sql.query_single(query)
					message = result
			if(id_from_name in dead_npcsid_in_room):
					message = "Here lies the dead body of'" + str(target) + "';" 
			else:
					message = "They're not here."
	elif(target in directions):
			message = "Everything looks great in that direction."
	elif(target == 'hell'):
			message = ""
	else:
		message = "Why would you look at that?"
	
	return message

	
## NOORA voit salee käyttää tätä tossa ylemmässä jos target on pelaajan location	
#No target, just looking around	
def look_around ():
	message = "You are in {0}.\n".format(sql.get_room_name(player.location))
	
	message += "You can move to:\n"
	passages = sql.get_adjacent_rooms(player.location)
	for item in passages:
		message += "\t{0}\n".format(sql.get_room_name(item))
	
	
	## elävät vaan nyt, pitää muuttaa
	npcs = sql.live_npcsid_in_room(player.location)
	if len(npcs) > 0:
		message += "These NPCS are here:\n"
		for id in npcs:
			id = id[0]
			message += "\t{0}\n".format(sql.npc_name_from_id(id))
	else:
		message += "There are no one here."
	return message

                
                
