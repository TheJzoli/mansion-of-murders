import mysql.connector

db= mysql.connector.connect(host="localhost",
                            user="pelaaja",
                            passwd="kana4",
                            db="mom_game",
                            buffered= True)
cur=db.cursor()
#sql
murderers = "SELECT npc.first_name, npc.last_name FROM mapped_npc INNER JOIN npc ON npc.npc_id = mapped_npc.npc ON mapped_npc.state = 'murdering';"
cur.execute(murderers)


#Blaming method : blame x of murdering y
def Blame(commands):
    if(commands[1] in murderers and commands[4] in dead_npcs):
        print("Correct the police will come to get the murderer.")
    else:
        print("Nope that's not right accusation.")
#synonyms, etc
blame_synonyms = ['accuse','blame','charge','allege']
fill_words = ['the','a','an','of']
murder_words = ['murdering','killing']
#if for blame
turn = 0
while turn < 3:
    command=input(">>> ")
    commands=command.lower().split(" ")
    cmd_len = len(commands)
    if(commands[0] in blame_synonyms):
        if(cmd_len > 1):
            if(commands[1] in live_npcs_in_room):
                if(cmd_len > 2):
                    if(commands[2] in fill_words):
                        if(cmd_len > 3):
                            if(commands[3] in murder_words):
                                if(cmd_len > 4):
                                    if(commands[4] in dead_npcs):
                                        Blame(commands)
                                        turn = turn + 1
                                    elif(commands[4] in live_npcs):
                                        print("They're not dead...")
                                    else:
                                        print("Why would you do that?")
                else:
                    print("Of murdering who?")
            elif(commands[1] in dead_npcs_in_room):
                 print("Don't blame the dead darling.")
            else:
                 print("You can't blame them.")
        else:
            print("Who are you blaming?")

                
