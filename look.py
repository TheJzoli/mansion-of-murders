'''
# These are all populated from master.py
rooms = [] 				# Names of rooms
npcs = []				# Npcs full name in list = ["firstname", "secondname"]
first_names = []		# only first names in list
last_names = []			# only last names in list
player					# player instance, holds location
'''
import sql

def all_npcids_in_room(room_id):
        query = "SELECT mapped_npc.mapped_id FROM npc, mapped_npc WHERE npc.npc_id = mapped_npc.npc AND mapped_npc.location = '" + str(room_id) + "';"
        result = sql.column_as_list(sql.run_query(query),0)
        return result

#No target, just looking around	
def look_around ():
	message = "You are in {0}.\n".format(sql.get_room_name(player.location))
	#siirretty
	query = "SELECT description FROM room WHERE room.room_id ='" + str(player.location) + "';"
	result = sql.query_single(query)
	#toimiiko tässä
	message += "You can move to:\n"
	passages = sql.get_adjacent_rooms(player.location)
	for item in passages:
		message += "\t{0}\n".format(sql.get_room_name(item))
	npcs = all_npcids_in_room(player.location)#dead or alive, muotoilu lauseeseen
	if len(npcs) > 0:
		message += "These people are here:\n"
		print(npcs)
		for item in npcs:
                        print(item)
                        message += "\t{0}\n".format(sql.npc_name_from_id(item))
	else:
		message += "There is no one else here."
	return message

def single_npc_description(id_from_name):
        query = "SELECT description FROM npc WHERE npc_id = " + str(id_from_name) + ";"
        result = sql.query_single(query)
        return result

def single_npc_details(target_id):
        #väärä
        query = "SELECT description FROM detail, npc_detail WHERE detail.detail_id = npc_detail.detail AND npc_detail.npc = '" + str(target_id) + "';"
        return column_as_list(run_query(query),0)

def look(target):
## mutta kun yrittää kattoo vaik 'look at benetton', niin sit tää sanoo, että se ei ole täällä
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
					details = single_npc_detail(target_id)#lista
					message += "\n They have the following details: \n"
					for detail in details:
                                                message += "\t{0}\n".format(detail)
					
			if(target_id in dead_npcsid_in_room):
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

                
                
