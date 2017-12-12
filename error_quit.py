import os
os.system('cls')
import random
import string

fore = ['\x1b[30m', '\x1b[34m', '\x1b[36m', '\x1b[32m', '\x1b[90m', '\x1b[94m',
'\x1b[96m', '\x1b[92m', '\x1b[95m', '\x1b[91m', '\x1b[97m', '\x1b[93m',
'\x1b[35m', '\x1b[31m', '\x1b[39m', '\x1b[37m', '\x1b[33m']

back = ['\x1b[40m', '\x1b[44m', '\x1b[46m', '\x1b[42m', '\x1b[100m', '\x1b[104m',
'\x1b[106m', '\x1b[102m', '\x1b[105m', '\x1b[101m', '\x1b[107m', '\x1b[103m',
'\x1b[45m', '\x1b[41m', '\x1b[49m', '\x1b[47m', '\x1b[43m']

#fore = list(range(30, 37)) + list(range(90, 97))
#back = list(range(40, 47)) + list(range(100, 107))


width = 90
height = 20


field = ""
for i in range(height):
	for j in range(width):
		f = random.choice (fore)
		b = random.choice (back)
		c = random.choice (string.punctuation)
		field += f + b + c
		
print (field)