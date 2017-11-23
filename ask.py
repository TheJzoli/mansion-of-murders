import sql

def ask(question):
	answer = ""
	if (question == 'alive'):
		answer = commands[3] + "? Who is that?"
	else:
		answer = "Well I remember that the murderer had..."
	return answer