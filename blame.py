def get_murder(id_m,id_v):
    query = "SELECT murderer, victim FROM murder WHERE murderer = '" + id_m + "' AND victim = '" + id_v + "';"
    result = sql.run_query(query)
    #rowcount?
    return rowcount

def murder_solved(id_m,id_v):
    query1 = "UPDATE murder SET solved = 1 WHERE murderer = '" + id_m + "' AND victim = '" + id_v + "';"
    sql.run_query(query1)
    query2 = "UPDATE mapped_npc SET state = 'arrested' WHERE mapped_id = '" + id_m + "';"
    sql.run_query(query2)
    #other updates?
    return

def escaper(id_m):
    query = "UPDATE mapped_npc SET state = 'escaped' WHERE mapped_id = '" + id_m + "';"
    sql.run_query(query)
    return

def victim_id (victim):
	query = "SELECT npc_id FROM murder INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.victim INNER JOIN npc ON npc.npc_id = mapped_npc.npc WHERE first_name = '{0}' AND last_name = '{1}';".format(victim[0], victim[1])
	return query_single(query)

def murderer_id(murderer):
    query = "SELECT npc_id FROM murder INNER JOIN mapped_npc ON mapped_npc.mapped_id = murder.murderer INNER JOIN npc ON npc.npc_id = mapped_npc.npc WHERE first_name = '{0}' AND last_name = '{1}';".format(murderer[0],murderer[1])
    return query_single(query)

def Blame(murderer,victim):
    message = ""
    id_m = murderer_id(murderer)
    id_v = victim_id(victim)
    murdercount = get_murder(id_m,id_v)
    if murdercount == 1:
        murder_solved(id_m,id_v)
        message = "Congratulations you solved a murder and the murderer will be arrested!"
    else:
        #(false = 0) ei voi tulla aina. while loopin alkuun?
        if false < 3:
            message = "Wrong accusation!"
            false = false + 1
        else:
            message = "Oh no too many false accusations! Now one of the real murderers escaped!"
            escaper(id_m)
            false = 0
    return message


