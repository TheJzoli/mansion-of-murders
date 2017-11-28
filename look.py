'''
# These are all populated from master.py
rooms = [] 				# Names of rooms
npcs = []
first_names = []
last_names = []
current_room = 1
'''
import sql
#vaihda first_name yms haku id

current_room_name = sql.get_room_name(player.location)

live_npcsid_in_room = sql.live_npcsid_in_room(player.location)

dead_npcsid_in_room = sql.dead_npcsid_in_room(player.location)

query = "SELECT first_name, last_name FROM npc WHERE npc_id ='" + live_npcsid_in_room + "';"
live_npcs_in_room =sql.run_query(query)

query ="SELECT first_name, last_name FROM npc WHERE npc_id ='" + dead_npcsid_in_room + "';"
dead_npcs_in_room = sql.run_query(query)

def id_from_name(mapped_id):
        query ="SELECT first_name, last_name FROM mapped_npc INNER JOIN npc ON 

def look(target):
        message = ""
        if(target in rooms):
                if(target in current_room_name):
                        query = "SELECT description FROM room WHERE name ='" + target + "';"
                        result = sql.query_single(query)
                        message = result
                else:
                        message = "You can't look there from here."
        elif(target in npcs):
                if(target in live_npcs_in_room):
                        query = "SELECT description FROM npc WHERE first_name ='" + target + "';"
                        result = sql.query_single(query)
                        message = result
                if(target in dead_npcs_in_room):
                        message = "Here lies the dead body of'" + target + "';" 
                else:
                        message = "They're not here."
        elif(target in directions):
                message = "Everything looks great in that direction."
        elif(target == 'hell'):
                message = ""
        else:
                message = "Why would you look at that?"
        return message
                
                

