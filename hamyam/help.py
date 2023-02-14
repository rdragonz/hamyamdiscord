def help(config):
	# Read and properly format the help from help.txt
	# Takes: none
	# Returns: Formatted text containing help file and current version string
	
	# Read help.txt file and send it as a Discord message.
	result = str()
	with open("help.txt", "r") as f:
		text = f.readlines()
		for line in text:
			result += line
	# Format Discord message and append version string
	text = """```{0}\n\n{1}\n```""".format(result, config.config["VERSION_STRING"])

	return text