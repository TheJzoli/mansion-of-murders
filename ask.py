def ask(question):
    if question == 'alive':
        fprint(commands[3] + "? Who is that?")
    else:
        fprint("Well I remember that the murderer had...")
def fprint(text):
    print(text)

Ask = ['ask', 'inquire', 'question']
Prepositions = ['about']
Murder = ['murder', 'case']

live_npcs_in_room = ['johnsson', 'petersson', 'kekkonen']
dead_npcs = ['deadman', 'youngman']

loop = True
invalid_command = False

while loop == True:
        
		if invalid_command == True:
            fprint("That doesn't make any sense")
        invalid_command = False
        command = input(">> ")
        commands = command.lower().split()
        cmd_len = len(commands)
        
        if (commands[0] in Ask):
            if (cmd_len > 1):
                if (commands[1] in live_npcs_in_room):
                    if (cmd_len > 2):
                        if (commands[2] in Prepositions):
                            if (commands[2] == 'about'):
                                if (cmd_len > 3):
                                    if (commands[3] in dead_npcs):
                                        if (cmd_len > 4):
                                            if (commands[4] in Murder):
                                                if (cmd_len > 5):
                                                    if (commands[5] == 'case'):
                                                        ask("dead")
                                                    else:
                                                        fprint("uuh what?")
                                                else:
                                                    ask("dead")
                                            else: #They ask about something other than murder
                                                fprint("Why would you want to ask that?")
                                        else: #If they ask without adding "murder" to the end
                                            ask("dead")
                                    else: #An NPC that is not dead
                                        ask("alive")
                                else: #If they only "Ask NPC about"
                                    fprint("About what?")
                            else: #They use the wrong preposition
                                fprint("Now that doesn't make any sense!")
                        else: #They don't use a preposition
                            invalid_command = True
                    else: #If they only "Ask NPC"
                        fprint("Ask what?")
                elif (commands[1] in dead_npcs): #They're a dead NPC
                    fprint("Dead men tell no tales...")
                else: #No NPC of that name in room
                    fprint("There is no such person here to talk to.")
            else: #If they only "Ask"
                fprint("Who?")
