def help(config):
	result = str()
	with open("help.txt", "r") as f:
		text = f.readlines()
		for line in text:
			result += line

	text = """```{0}\n\n{1}\n```""".format(result, config.config["VERSION_STRING"])

	return text