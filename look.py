'''
# These are all populated from master.py
rooms = []              # Names of rooms
npcs = []               # Npcs full name in list = ["firstname", "secondname"]
player                  # player instance, holds location
'''

import sql
from common import *

def all_npcids_in_room(room_id):
        query = "SELECT mapped_npc.mapped_id FROM npc, mapped_npc WHERE npc.npc_id = mapped_npc.npc AND mapped_npc.location = '" + str(room_id) + "';"
        result = sql.column_as_list(sql.run_query(query),0)
        return result

def look_around ():
	message = "You are in {0}.\n".format(sql.get_room_name(player.location))
	query = "SELECT description FROM room WHERE room.room_id ='" + str(player.location) + "';"
	result = sql.query_single(query)

	message += "You can move to:\n"

	#---------------------------
	passages = sql.get_adjacent_rooms_and_directions(player.location)

	room_names = []
	directions = []
	longest_length = 0
	count = 0
	
	for item in passages:
		room_names.append(sql.room_name_from_id(item [0]))
		length = len(room_names[-1])
		if length > longest_length:
			longest_length = length
		directions.append (sql.long_direction(item[1]))
		count += 1
		
	for i in range(count):
		message += "@i\t{0:{1}}\t{2}\n".format(room_names[i], longest_length + 2, directions[i])
	#-----------------------------


	live_npcs = sql.live_npcsid_in_room(player.location)
	dead_npcs = sql.dead_npcsid_in_room(player.location)
	total_npcs = len (live_npcs) + len (dead_npcs)
	if total_npcs > 0:
		message += "These people are here:\n"
		for item in live_npcs:
			formatted_name = format_npc(sql.npc_name_from_id(item))
			message +="@i\t{0}\n".format(formatted_name)
		if len(dead_npcs) > 0:
			message += "But these people seem to be dead!:\n"
			for item in dead_npcs:
				formatted_name = format_npc (sql.npc_name_from_id(item))
				message +="@i\t{0}\n".format(formatted_name)
				sql.add_player_clue(item, None)
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
		
def arrested_npcs():
	query = "SELECT mapped_id FROM mapped_npc WHERE state = 'arrested';"
	return sql.column_as_list(sql.run_query(query),0)

def escaped_npcs():
	query = "SELECT mapped_id FROM mapped_npc WHERE state = 'escaped';"
	return sql.column_as_list(sql.run_query(query),0)

def look(target):


	live_npcsid_in_room = sql.live_npcsid_in_room(player.location)
	dead_npcsid_in_room = sql.dead_npcsid_in_room(player.location)
	arrested = arrested_npcs()
	escaped = escaped_npcs()

	message = ""
	if(target in sql.get_rooms()):
			
		room_id = sql.get_room_id(target)
		if(room_id == player.location):
			message = look_around()
			if message == None:
				message = "{0} is rather nice.".format(target)
		else:
				message = "You cannot see there from here."
				
	elif(target in sql.get_npcs()):

		target_id = sql.npc_id_from_name(target)
		if(target_id in live_npcsid_in_room):
				
			message = single_npc_description(target_id)

			details = single_npc_details(target_id)
			if len(details) > 0:
				message += "\nYou immediately notice these striking details about them:"
				for detail in details:
					message += "\n@i\t{0}".format(detail)

		elif(target_id in dead_npcsid_in_room):
			message = "Here lies the dead body of " + format_npc(target) + ". How sad indeed..." 
			
		elif(target_id in arrested):
			message = "They've already been arrested and taken away."
			
		elif(target_id in escaped):
			message = "Oh no looks like they've escaped."

		else:
			message = "They're not here."
			
	elif (target in sql.get_all_directions()):
		room_in_direction = sql.get_room_in_direction(player.location, target)
		if room_in_direction:
			room_name = format_room(sql.room_name_from_id(room_in_direction))
			message = "You see the {0} in {1}.".format(room_name, sql.long_direction(target))
		else:
			message = "There's some tastefully arranged interior art there. Very apprecietable!"
	
	elif target == 'notes':
		notes = sql.get_notes()
		message = "NOTES:\n"
		if len (notes) > 0:
			for entry in notes:
				if entry [3]:
					message += "\nSOLVED" + expired_colour
				victim_name = format_npc(sql.npc_name_from_id(entry[0]))
				room_name = format_room(sql.room_name_from_id(entry[1]))
				message += "\n{0} was killed in the {1}.".format(victim_name, room_name)
				if entry [2]:
					message += " Clues about their killer:"
					for item in entry[2]:
						message += "\n@i\t{0}".format(sql.detail_name_from_id(item))

				if entry[3]:
					message += default_colour
				message += "\n"
				
			# Slice away last newline
			message = message[:-1]
			
		else:
			message += "@i\tno notes yet"
			
	elif(target == 'hell'):
		message = "Looks like you looked right into your future."

	else:
		message = "Why would you look at that?"

	return message

                
                
