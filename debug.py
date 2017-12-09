from inspect import getframeinfo, stack
def DEBUG (message):
	debug = False
	if debug:
		caller = getframeinfo(stack()[1][0])
		print ("DEBUG [{0}: {1}]: {2}".format(caller.filename.split(sep="\\")[-1], caller.lineno, message))