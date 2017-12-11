wordsfile = open(r"C:\Users\Joel\Documents\GitHub\mansion-of-murders\words.txt")
words = wordsfile.read()
lines = words.split(sep="\n")

verbs = [lines[i].split()[1] for i in range (len(lines))]

printout = ""
for item in verbs:
	printout += "INSERT INTO all_verbs VALUES ('{0}');\n".format(item)
print(printout)
input()