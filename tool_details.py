# Detail Tool
# ©Leo Tamminen

import random;

people = 20
details = 20
details_per_person = 5

detail_lists = []

for i in range (people):
	detail_list = []
	for j in range (details):
		detail_list.append (j + 1)

	for k in range (details):
		random_position = random.randint(k, details - 1)
		detail_list [k], detail_list [random_position] = detail_list [random_position], detail_list [k]

	detail_lists.append ([])
	for m in range (details_per_person):
		detail_lists [i].append (detail_list[m])
	
for m in range (people):
	person = m + 1

	detail_lists [m].sort()
	for n in range (details_per_person):
		detail = detail_lists [m] [n]
		print ("INSERT INTO npc_detail VALUES ({0}, {1});".format (person, detail))