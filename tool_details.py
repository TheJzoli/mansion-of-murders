# Detail Tool
# ©Leo Tamminen

import random
import math

import mysql.connector
database = mysql.connector.connect(
					host = 'localhost',
					user = 'dbuser',
					passwd = 'dbpass',
					db = 'mom_game',
					buffered = True)
cursor = database.cursor()


def get_groups(groups):
	for i in range (len(groups)):
		cursor.execute("SELECT npc_id FROM npc WHERE map_group = '{0}' AND sub_group = {1};".format(groups[i][0], groups[i][1]))
		result = cursor.fetchall()
		
		list = []
		for record in result:
			list.append(record[0])
		
		yield list

def shuffle (source):
	count = len(source)
	result = list(source)
	for i in range (count - 1):
		random_index = random.randint(i, count - 1)
		result[i], result[random_index] = result[random_index], result[i]
	return result
	
def shuffled_details (source):
	details = shuffle(source)
	for item in details:
		yield item
		
group_ids_a = ['A1', 'A2', 'A3', 'A4', 'A5']
groups_a = []
for item in get_groups(group_ids_a):
	groups_a.append (item)
	
group_ids_b = ['B1', 'B2', 'B3', 'B4', 'B5']
groups_b = []	
for item in get_groups(group_ids_b):
	groups_b.append (item)

	
cursor.execute("SELECT COUNT(*) FROM detail")	
number_details = cursor.fetchall()[0][0]

half = math.ceil(number_details / 2)
details = []
for i in range (1, number_details + 1):
	details.append(i)

details_a = details [:half]
details_b = details [half:]

details_per_npc = 5
npc_details = []

for group in groups_a:
	details = shuffled_details(details_a)
	for npc in group:
		for _ in range (details_per_npc):
			npc_details.append((npc, details.__next__()))

for group in groups_b:
	details = shuffled_details(details_b)
	for npc in group:
		for _ in range (details_per_npc):
			npc_details.append ((npc, details.__next__()))
			

printout = ""
for item in sorted(npc_details):
	printout += "INSERT INTO npc_detail VALUES ({0:3}, {1:3});\n".format(item[0], item[1])
print (printout)
	
'''
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
		
'''