'''
# These are all populated from master.py
rooms = []              # Names of rooms
npcs = []               # Npcs full name in list = ["firstname", "secondname"]
first_names = []        # only first names in list
last_names = []         # only last names in list
player                  # player instance, holds location
'''
import sql
import formatter

def DEBUG(message):
	print ("LOOK DEBUG: " + str(message))

def all_npcids_in_room(room_id):
        query = "SELECT mapped_npc.mapped_id FROM npc, mapped_npc WHERE npc.npc_id = mapped_npc.npc AND mapped_npc.location = '" + str(room_id) + "';"
        result = sql.column_as_list(sql.run_query(query),0)
        return result

def look_around ():
    message = "You are in {0}.\n".format(sql.get_room_name(player.location))
    query = "SELECT description FROM room WHERE room.room_id ='" + str(player.location) + "';"
    result = sql.query_single(query)
    
    message += "You can move to:\n"
    passages = sql.get_adjacent_rooms(player.location)
    for item in passages:
        message += "\t{0}\n".format(sql.get_room_name(item))#and direction, uusi sql? name + direction
        
    npcs = all_npcids_in_room(player.location)
    dead = sql.dead_npcsid_in_room(player.location)
    if len(npcs) > 0:
                message += "These people are here:\n"
                for item in npcs:
                        message +="\t{0}\n".format(sql.npc_name_from_id(item))#nimen muotoilut
                if len(dead) > 0:
                        message += "But these people seem to be dead!:\n"
                        for item in dead:
                                message += "\t{0}\n".format(sql.npc_name_from_id(item))
    else:
        message += "There is no one in here."

    return message

def single_npc_description(id_from_name):
        query = "SELECT description FROM npc WHERE npc_id = " + str(id_from_name) + ";"
        result = sql.query_single(query)
        return result

def single_npc_details(target_id):
        query = (
				"SELECT detail.name from detail, npc_detail,mapped_npc "
				"WHERE detail.detail_id = npc_detail.detail "
				"AND npc_detail.npc = mapped_npc.npc "
				"AND mapped_npc.mapped_id = '"
				) + str(target_id) + "';"
        return sql.column_as_list(sql.run_query(query),0)

def look(target):

	live_npcsid_in_room = sql.live_npcsid_in_room(player.location)
	dead_npcsid_in_room = sql.dead_npcsid_in_room(player.location)

	message = ""
	if(target in rooms):
			
		room_id = sql.get_room_id(target)

		if(room_id == player.location):
			message = look_around()
			if message == None:
				message = "{0} is rather nice.".format(target)
		else:
				message = "You can't look there from here."
	elif(target in npcs):

		target_id = sql.npc_id_from_name(target)
		print(sql.room_name_from_id(player.location))
		for npc in live_npcsid_in_room:
			print(sql.npc_name_from_id(npc))

		if(target_id in live_npcsid_in_room):
				
			message = single_npc_description(target_id)

			details = single_npc_details(target_id)
			if len(details) > 0:
				message += "You immediately notice these striking details about them:\n"#ongelma
				for detail in details:
					message += "\t{0}\n".format(detail)

		elif(target_id in dead_npcsid_in_room):
			message = "Here lies the dead body of'" + str(target) + "'. How sad indeed..." 

		else:
			message = "They're not here."
	elif(target in directions):#mikä huone suunnassa
		message = "Everything looks great in that direction."
	elif target == 'notes':
#	def view_notes ():
		notes = sql.get_notes()
		message = "NOTES:\n\n"
		for entry in notes:
			victim = formatter.name(sql.npc_name_from_id(entry[0]))
			room = formatter.room(sql.room_name_from_id(entry[1]))
			message += "{0} was killed in {1}. Clues about their killer:\n".format(victim, room)
			for item in entry[2]:
				message += "\t{0}\n".format(sql.detail_name_from_id(item))
			#fprint (printout)
#		message = view_notes()
	elif(target == 'hell'):
		message = "Looks like you looked right into your future."

	else:
		message = "Why would you look at that?"

	return message

                
                
