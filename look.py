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
get_room_id = sql.get_room_id
id_from_name = sql.id_from_name

def look(target):
        message = ""
        if(target in rooms):
                room_id = sql.get_room_id(target)
                if(room_id == current_room):
                        query = "SELECT description FROM room WHERE room.room_id ='" + room_id + "';"
                        result = sql.query_single(query)
                        message = result
                else:
                        message = "You can't look there from here."
        elif(target in npcs):
                
                npc_id = sql.id_from_name(target)
                live_npc_id_in_room = sql.live_in_room(npc_id)
                dead_npc_id_in_room = sql.dead_in_room(npc_id)
                
                if(npc_id in live_npc_id_in_room):
                        query = "SELECT description FROM npc WHERE npc_id ='" + npc_id + "';"
                        result = sql.query_single(query)
                        message = result
                if(npc_id in dead_npc_id_in_room):
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
                
                
