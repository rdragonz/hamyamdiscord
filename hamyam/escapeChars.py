def escapeChars(txt):
	# Escape potentially unsafe characters
	# Takes: Input text
	# Returns: String containing escaped characters
	
	message = txt
	temp = message.replace('-', '\-')
	temp = temp.replace('.', '\.')
	temp = temp.replace('#', '\#')
	temp = temp.replace('(', '\(')
	temp = temp.replace('=', '\=')
	temp = temp.replace(')', '\)')
	temp = temp.replace('+', '\+')
	temp = temp.replace('!', '\!')
	return temp