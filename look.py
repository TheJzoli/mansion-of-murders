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
def get_room_id(target):
        query = "SELECT room.room_id FROM room WHERE room.name ='" + target + "';"
        room_id = sql.query_single(query)
        return room_id

def id_from_name(target):
        #first_name = target?? 
        query ="SELECT npc_id FROM mapped_npc INNER JOIN npc ON mapped_npc.npc = npc.npc_id WHERE npc.first_name ='" + target + "';"
        npc_id = sql.query_single(query)
        return npc_id

def live_in_room(npc_id):
        query = "SELECT npc.npc_id FROM npc WHERE npc.npc_id NOT IN(SELECT npc.npc_id FROM murder INNER JOIN mapped_npc ON mapped_npc.npc = murder.victim INNER JOIN npc ON npc.npc_id = mapped_npc.npcWHERE mapped_npc.location = '" + current_room + "');"
        live_id = sql.run_query(query)
        return live_id

def dead_in_room(npc_id):
        query= "SELECT npc.npc_id FROM murder INNER JOIN mapped_npc ON mapped_npc.npc = murder.victim INNER JOIN npc ON npc.npc_id = mapped_npc.npc WHERE mapped_npc.location ='" + current_room + "';"
        dead_id = sql.run_query(query)
        return dead_id

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
                
                
