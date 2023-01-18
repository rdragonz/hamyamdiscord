def escapeChars(txt):
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