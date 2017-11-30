'''
# These are all populated from master.py
rooms = [] 				# Names of rooms
npcs = []
first_names = []
last_names = []
current_room = 1
'''
import sql

#onko jo olemassa

live_npcsid_in_room = sql.live_npcsid_in_room(player.location)
dead_npcsid_in_room = sql.dead_npcsid_in_room(player.location)
get_room_id = sql.get_room_id(player.location)
id_from_name = sql.id_from_name(target)

def look(target):
        message = ""
        if(target in rooms):
                
                if(get_room_id == player.location):
                        query = "SELECT description FROM room WHERE room.room_id ='" + get_room_id + "';"
                        result = sql.query_single(query)
                        message = result
                else:
                        message = "You can't look there from here."
        elif(target in npcs):
                
                if(id_from_name in live_npcsid_in_room):
                        query = "SELECT description FROM npc WHERE npc_id ='" + id_from_name + "';"
                        result = sql.query_single(query)
                        message = result
                if(id_from_name in dead_npcsid_in_room):
                        message = "Here lies the dead body of'" + target + "';" 
                else:
                        message = "They're not here."
        elif(target in directions):
                message = "Everything looks great in that direction."
        elif(target == hell):
                message = ""
        else:
                message = "Why would you look at that?"
        return message
                
                
