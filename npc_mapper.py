import random;

npcs_amount = 20
npc_indices = []

for i in range (npcs_amount):
	npc_indices.append(i + 1)

#fischer-yates shuffle
for i in range (npcs_amount):
	random_position = random.randint (i, npcs_amount - 1)
	npc_indices[i], npc_indices [random_position] = npc_indices[random_position], npc_indices [i]


room = 1
for i in range (npcs_amount):
	id  = i + 1
	if id % 10 == 0:
		murderer_state = "murdering"
	else:
		murderer_state = "not murderer"
	print("INSERT INTO mapped_npc VALUES ({0}, {1}, {2}, '{3}');".format(id, npc_indices[i], room, murderer_state))